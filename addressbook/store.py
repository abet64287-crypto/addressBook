"""SQLite persistence. Imports are committed as one transaction."""
import json
import sqlite3
from contextlib import closing
from pathlib import Path

from werkzeug.exceptions import NotFound


def connect(path):
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    return db


def initialize(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with closing(connect(path)) as db, db:
        db.execute('CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY AUTOINCREMENT, data TEXT NOT NULL)')


def decode(row):
    return dict(json.loads(row['data']), id=row['id'])


def list_contacts(path):
    with closing(connect(path)) as db:
        return [decode(row) for row in db.execute('SELECT * FROM contacts ORDER BY id DESC')]


def save(path, contact, contact_id=None):
    with closing(connect(path)) as db, db:
        if contact_id is None:
            contact_id = db.execute('INSERT INTO contacts(data) VALUES (?)',
                                    (json.dumps(contact, ensure_ascii=False),)).lastrowid
        else:
            changed = db.execute('UPDATE contacts SET data=? WHERE id=?',
                                 (json.dumps(contact, ensure_ascii=False), contact_id)).rowcount
            if not changed:
                raise NotFound()
    return dict(contact, id=contact_id)


def set_favorite(path, contact_id, value):
    with closing(connect(path)) as db, db:
        row = db.execute('SELECT * FROM contacts WHERE id=?', (contact_id,)).fetchone()
        if row is None:
            raise NotFound()
        contact = json.loads(row['data'])
        contact['favorite'] = value
        db.execute('UPDATE contacts SET data=? WHERE id=?', (json.dumps(contact, ensure_ascii=False), contact_id))
    return dict(contact, id=contact_id)


def delete(path, contact_id):
    with closing(connect(path)) as db, db:
        if not db.execute('DELETE FROM contacts WHERE id=?', (contact_id,)).rowcount:
            raise NotFound()


def fingerprint(contact):
    # Exact data match, ignoring method order. Same names alone are not duplicates.
    copy = {k: v for k, v in contact.items() if k != 'id'}
    copy['methods'] = sorted(copy['methods'], key=lambda m: (m['type'], m['label'], m['value']))
    return json.dumps(copy, sort_keys=True, ensure_ascii=False)


def import_contacts(path, contacts):
    with closing(connect(path)) as db, db:
        known = {fingerprint(decode(row)) for row in db.execute('SELECT * FROM contacts')}
        imported = 0
        for contact in contacts:
            key = fingerprint(contact)
            if key in known:
                continue
            db.execute('INSERT INTO contacts(data) VALUES (?)', (json.dumps(contact, ensure_ascii=False),))
            known.add(key)
            imported += 1
    return dict(imported=imported, skipped=len(contacts) - imported, total=len(contacts))
