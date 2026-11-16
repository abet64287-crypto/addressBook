import pytest
from addressbook import create_app
from seed_demo import DEMO

HEADERS = {"X-Requested-With": "AddressBook"}


def test_home_and_empty_state(client):
    response = client.get('/')
    assert response.status_code == 200
    assert 'Address Book' in response.text
    assert client.get('/api/contacts').json == []
    assert client.get('/static/app.js').status_code == 200


def test_crud_and_persistence(client, app):
    created = client.post('/api/contacts', json=DEMO[0], headers=HEADERS)
    assert created.status_code == 201
    contact = created.json
    assert len(contact['methods']) == 6
    assert contact['favorite']
    identifier = contact['id']
    other = create_app({'TESTING': True, 'DATABASE': app.config['DATABASE']}).test_client()
    assert other.get('/api/contacts').json == [contact]
    assert client.patch(f'/api/contacts/{identifier}/favorite', json={'favorite': False}, headers=HEADERS).json['favorite'] is False
    contact['name'] = '已修改'
    contact['methods'].pop()
    assert client.put(f'/api/contacts/{identifier}', json=contact, headers=HEADERS).json['name'] == '已修改'
    assert client.delete(f'/api/contacts/{identifier}', headers=HEADERS).status_code == 204
    assert client.get('/api/contacts').json == []
    assert client.delete(f'/api/contacts/{identifier}', headers=HEADERS).status_code == 404


@pytest.mark.parametrize('payload', [None, [], {}, {'name': ' '}, {'name': 'A', 'favorite': 'true'},
    {'name': 'A', 'methods': [{'type': 'fax', 'value': '1'}]},
    {'name': 'A', 'methods': [{'type': [], 'value': '1'}]},
    {'name': 'A', 'methods': [{'type': 'email', 'value': 'invalid'}]},
    {'name': 'A', 'methods': [{'type': 'phone', 'value': ''}]},
    {'name': 'A', 'methods': [{'type': 'phone', 'value': '1'}] * 31}])
def test_invalid_contacts(client, payload):
    assert client.post('/api/contacts', json=payload, headers=HEADERS).status_code in {400, 415}


def test_write_protection(client):
    assert client.post('/api/contacts', json=DEMO[0]).status_code == 400
    assert client.post('/api/contacts', json=DEMO[0], headers={**HEADERS, 'Origin': 'https://elsewhere.example'}).status_code == 400
    assert client.patch('/api/contacts/100/favorite', json={'favorite': True}, headers=HEADERS).status_code == 404
    assert client.patch('/api/contacts/100/favorite', json={}, headers=HEADERS).status_code == 400


