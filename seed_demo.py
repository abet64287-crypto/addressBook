"""Explicitly insert fictional demo records; never replace existing data."""
from addressbook import create_app, store
from addressbook.domain import validate_contact

DEMO = [
    dict(name='Alex Lin', company='Design Studio', group='Work', favorite=True, notes='Project meeting on Wednesday.', methods=[
        dict(type='phone', label='Work', value='00123456789'), dict(type='phone', label='Other', value='+86 010 55550001'),
        dict(type='email', label='Work', value='zhixia@example.com'), dict(type='email', label='Personal', value='lin@example.org'),
        dict(type='social', label='WeChat', value='demo_zhixia'), dict(type='address', label='Office', value='12 Example Road')]),
    dict(name='Chris Chen', company='Example Technology', group='Work', favorite=True, notes='Product requirements contact.', methods=[dict(type='email',label='Work',value='chenxu@example.com')]),
    dict(name='Taylor Xu', company='University', group='Friends', favorite=False, notes='Course project teammate.', methods=[dict(type='social',label='WeChat',value='demo_qinghe')]),
    dict(name='Jordan Zhou', company='Photographer', group='Friends', favorite=False, notes='', methods=[dict(type='phone',label='Mobile',value='00123456780')]),
    dict(name='Sam Lu', company='Bookstore', group='Services', favorite=False, notes='Weekend reading group.', methods=[dict(type='email',label='Events',value='books@example.com')]),
]

if __name__ == '__main__':
    app = create_app()
    result = store.import_contacts(app.config['DATABASE'], [validate_contact(c) for c in DEMO])
    print(f"Demo data: imported {result['imported']}; skipped {result['skipped']}.")
