from addressbook import create_app


def test_environment_database_path(tmp_path, monkeypatch):
    database = tmp_path / 'persistent' / 'contacts.sqlite3'
    monkeypatch.setenv('ADDRESSBOOK_DATABASE', str(database))
    app = create_app({'TESTING': True})
    assert app.config['DATABASE'] == str(database)
    assert database.exists()
    assert app.test_client().get('/api/health').json == {'status': 'ok'}


def test_explicit_database_overrides_environment(tmp_path, monkeypatch):
    monkeypatch.setenv('ADDRESSBOOK_DATABASE', str(tmp_path / 'env.sqlite3'))
    app = create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'explicit.sqlite3')})
    assert app.config['DATABASE'] == str(tmp_path / 'explicit.sqlite3')
    assert not (tmp_path / 'env.sqlite3').exists()


def test_https_same_origin_write(tmp_path):
    # Waitress --url-scheme=https supplies this external scheme behind Caddy.
    app = create_app({'TESTING': True, 'DATABASE': str(tmp_path / 'contacts.sqlite3')})
    client = app.test_client()
    headers = {'X-Requested-With': 'AddressBook', 'Origin': 'https://contacts.calculator-demo.site'}
    response = client.post('/api/contacts', base_url='https://contacts.calculator-demo.site',
                           json={'name': 'Cloud Demo'}, headers=headers)
    assert response.status_code == 201
    headers['Origin'] = 'https://elsewhere.example'
    assert client.post('/api/contacts', base_url='https://contacts.calculator-demo.site',
                       json={'name': 'Blocked'}, headers=headers).status_code == 400
