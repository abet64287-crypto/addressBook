"""Member B: Excel endpoints, integrated by the application factory."""
from io import BytesIO

from flask import Blueprint, current_app, jsonify, request, send_file

from . import store
from .domain import ValidationError
from .excel import export_contacts, parse_workbook

excel_api = Blueprint('excel', __name__)


@excel_api.get('/api/export')
@excel_api.get('/api/template')
def export():
    template = request.path.endswith('template')
    contacts = [] if template else store.list_contacts(current_app.config['DATABASE'])
    return send_file(BytesIO(export_contacts(contacts)), as_attachment=True,
                     download_name='contacts-template.xlsx' if template else 'contacts.xlsx',
                     mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


@excel_api.post('/api/import')
def import_excel():
    upload = request.files.get('file')
    if not upload or not upload.filename or not upload.filename.lower().endswith('.xlsx'):
        raise ValidationError('Please select an .xlsx file.')
    contacts = parse_workbook(upload.stream)
    return jsonify(store.import_contacts(current_app.config['DATABASE'], contacts))
