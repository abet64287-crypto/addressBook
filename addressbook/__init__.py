"""Address book application factory and HTTP routes."""
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import HTTPException

from . import store
from .domain import ValidationError, validate_contact
from .excel_routes import excel_api


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(DATABASE=os.environ.get('ADDRESSBOOK_DATABASE') or str(Path(app.instance_path) / 'contacts.sqlite3'),
                      MAX_CONTENT_LENGTH=10 * 1024 * 1024)
    if config:
        app.config.update(config)
    store.initialize(app.config['DATABASE'])

    @app.before_request
    def protect_writes():
        if request.method in {'POST', 'PUT', 'PATCH', 'DELETE'}:
            if request.headers.get('X-Requested-With') != 'AddressBook':
                raise ValidationError('Please use the application interface.')
            origin = request.headers.get('Origin')
            if origin and origin != request.host_url.rstrip('/'):
                raise ValidationError('Cross-origin writes are not allowed.')

    @app.errorhandler(ValidationError)
    def invalid(exc):
        return jsonify(error=str(exc)), 400

    @app.errorhandler(HTTPException)
    def http_error(exc):
        messages = {404: 'Contact or page not found.', 413: 'File exceeds the 10 MB limit.',
                    400: 'Invalid request. Please check your input.', 405: 'Method not allowed.'}
        return jsonify(error=messages.get(exc.code, exc.description)), exc.code

    @app.after_request
    def response_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Cache-Control'] = 'no-store'
        response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; frame-ancestors 'none'"
        return response

    @app.get('/')
    def home():
        return render_template('index.html')

    @app.get('/api/contacts')
    def contacts():
        return jsonify(store.list_contacts(app.config['DATABASE']))

    @app.get('/api/health')
    def health():
        return jsonify(status='ok')

    @app.post('/api/contacts')
    def create():
        contact = validate_contact(request.get_json())
        return jsonify(store.save(app.config['DATABASE'], contact)), 201

    @app.put('/api/contacts/<int:contact_id>')
    def update(contact_id):
        contact = validate_contact(request.get_json())
        return jsonify(store.save(app.config['DATABASE'], contact, contact_id))

    @app.patch('/api/contacts/<int:contact_id>/favorite')
    def favorite(contact_id):
        payload = request.get_json()
        if not isinstance(payload, dict) or type(payload.get('favorite')) is not bool:
            raise ValidationError('Favorite must be a boolean.')
        return jsonify(store.set_favorite(app.config['DATABASE'], contact_id, payload['favorite']))

    @app.delete('/api/contacts/<int:contact_id>')
    def delete(contact_id):
        store.delete(app.config['DATABASE'], contact_id)
        return '', 204

    app.register_blueprint(excel_api)

    return app
