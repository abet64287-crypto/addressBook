from io import BytesIO
from openpyxl import Workbook, load_workbook
import pytest
from addressbook import create_app
from seed_demo import DEMO

HEADERS = {"X-Requested-With": "AddressBook"}


def upload(client, content, filename='contacts.xlsx'):
    return client.post('/api/import', headers=HEADERS,
                       data={'file': (BytesIO(content), filename)})


def workbook(rows):
    book = Workbook()
    for row in rows:
        book.active.append(row)
    stream = BytesIO()
    book.save(stream)
    book.close()
    return stream.getvalue()


def test_excel_round_trip(client, tmp_path):
    for item in DEMO:
        assert client.post('/api/contacts', json=item, headers=HEADERS).status_code == 201
    exported = client.get('/api/export')
    assert exported.status_code == 200
    assert exported.data[:2] == b'PK'
    book = load_workbook(BytesIO(exported.data))
    rows = list(book.active.values)
    assert len(rows) == len(DEMO) + 1
    assert 'Phone2' in rows[0] and 'Email2Label' in rows[0]
    book.close()
    second = create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'second.sqlite3')}).test_client()
    result = upload(second, exported.data)
    assert result.json == {'imported': 5, 'skipped': 0, 'total': 5}
    def normalize(items):
        return {c['name']: {**c, 'id': None} for c in items}
    assert normalize(second.get('/api/contacts').json) == normalize(client.get('/api/contacts').json)
    assert upload(second, exported.data).json['skipped'] == 5


def test_text_values_and_formula_like_text(client):
    person = {**DEMO[0], 'name': '=HYPERLINK("https://example.com")', 'notes': '+1\n中文备注'}
    client.post('/api/contacts', json=person, headers=HEADERS)
    data = client.get('/api/export').data
    book = load_workbook(BytesIO(data), data_only=False)
    assert book.active['A2'].data_type == 's'
    assert book.active['F2'].value == '00123456789'
    book.close()
    assert upload(client, data).json['skipped'] == 1


@pytest.mark.parametrize('rows, fragment', [
    ([['公司'], ['示例公司']], 'Name'),
    ([['姓名', '姓名'], ['A', 'B']], 'duplicate'),
    ([['姓名', '未知列'], ['A', 'B']], 'Unsupported column'),
    ([['姓名', '邮箱1'], ['正常', 'a@example.com'], ['错误', 'invalid']], 'Row 3'),
    ([['姓名', '电话1'], ['正常', '00123'], ['', '00124']], 'Row 3'),
    ([['姓名', '收藏'], ['A', 'maybe']], 'Favorite'),
    ([['姓名'], ['=1+1']], 'formulas'),
    ([['姓名', '电话1标签'], ['A', '工作']], 'missing its value'),
    ([['姓名', '电话1', '电话1标签'], ['A', '', '工作']], 'no value'),
])
def test_atomic_invalid_import(client, rows, fragment):
    response = upload(client, workbook(rows))
    assert response.status_code == 400
    assert fragment in response.json['error']
    assert client.get('/api/contacts').json == []


def test_duplicate_policy(client):
    data = workbook([['姓名', '电话1'], ['同名', '001'], ['同名', '002'], ['同名', '001']])
    assert upload(client, data).json == {'imported': 2, 'skipped': 1, 'total': 3}


def test_invalid_files_and_template(client):
    assert upload(client, b'not excel').status_code == 400
    assert upload(client, b'not excel', 'contacts.csv').status_code == 400
    assert upload(client, client.get('/api/template').data).json['imported'] == 0
    assert client.post('/api/import', headers=HEADERS).status_code == 400


def test_excel_upload_limits(client):
    assert upload(client, b'x' * (10 * 1024 * 1024 + 1)).status_code == 413
    assert upload(client, workbook([['姓名']] + [['A']] * 1001)).status_code == 400


