"""Shared validation for both forms and spreadsheets."""
import re

TYPES = {'phone': 'Phone', 'email': 'Email', 'social': 'Social', 'address': 'Address'}


class ValidationError(ValueError):
    pass


def text(value, field, limit, required=False):
    if not isinstance(value, str):
        raise ValidationError(f'{field} must be text.')
    value = value.strip()
    if required and not value:
        raise ValidationError(f'{field} is required.')
    if len(value) > limit:
        raise ValidationError(f'{field} must not exceed {limit} characters.')
    if any(ord(c) < 32 and c not in '\t\n\r' for c in value):
        raise ValidationError(f'{field} contains unsupported control characters.')
    return value


def validate_contact(data):
    if not isinstance(data, dict):
        raise ValidationError('Invalid contact data.')
    result = {key: text(data.get(key, ''), label, limit, key == 'name')
              for key, label, limit in [('name', 'Name', 100), ('company', 'Company', 200),
                                        ('group', 'Group', 100), ('notes', 'Notes', 2000)]}
    favorite = data.get('favorite', False)
    if type(favorite) is not bool:
        raise ValidationError('Favorite must be a boolean.')
    result['favorite'] = favorite
    methods = data.get('methods', [])
    if not isinstance(methods, list) or len(methods) > 120:
        raise ValidationError('Contact methods must be a list of at most 120 items.')
    result['methods'] = []
    counts = dict.fromkeys(TYPES, 0)
    for item in methods:
        if not isinstance(item, dict) or not isinstance(item.get('type'), str) or item['type'] not in TYPES:
            raise ValidationError('Unsupported contact method type.')
        kind = item['type']
        counts[kind] += 1
        if counts[kind] > 30:
            raise ValidationError('Each method type supports up to 30 entries.')
        value = text(item.get('value', ''), TYPES[kind], 1000, True)
        label = text(item.get('label', ''), 'Label', 50)
        if kind == 'email' and not re.fullmatch(r'[^\s@]+@[^\s@]+\.[^\s@]+', value):
            raise ValidationError('Email format is invalid.')
        result['methods'].append(dict(type=kind, label=label, value=value))
    return result
