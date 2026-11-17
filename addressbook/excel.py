"""One contact per Excel row; indexed columns preserve method labels."""
from io import BytesIO
import re
from zipfile import ZipFile, BadZipFile

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

from .domain import TYPES, ValidationError, validate_contact

BASE = ['Name', 'Company', 'Group', 'Favorite', 'Notes']
PATTERN = re.compile(r'^(Phone|Email|Social|Address)([1-9][0-9]?)(Label)?$')


def normalize_header(header):
    aliases = {'姓名': 'Name', '公司': 'Company', '分组': 'Group', '收藏': 'Favorite', '备注': 'Notes', '电话': 'Phone', '邮箱': 'Email', '社交账号': 'Social', '地址': 'Address', '标签': 'Label'}
    for old, new in aliases.items():
        header = header.replace(old, new)
    return header


def export_contacts(contacts):
    sizes = {kind: max([1] + [sum(m['type'] == kind for m in c['methods']) for c in contacts]) for kind in TYPES}
    headers = BASE.copy()
    for kind, label in TYPES.items():
        for i in range(1, sizes[kind] + 1):
            headers.extend([f'{label}{i}', f'{label}{i}Label'])
    book = Workbook()
    sheet = book.active
    sheet.title = 'Contacts'
    sheet.append(headers)
    for c in contacts:
        values = [c['name'], c['company'], c['group'], 'Yes' if c['favorite'] else 'No', c['notes']]
        for kind in TYPES:
            methods = [m for m in c['methods'] if m['type'] == kind]
            for i in range(sizes[kind]):
                values.extend([methods[i]['value'], methods[i]['label']] if i < len(methods) else ['', ''])
        sheet.append(values)
        for cell in sheet[sheet.max_row]:
            cell.data_type = 's'
            cell.number_format = '@'
            cell.alignment = Alignment(vertical='top', wrap_text=True)
    for cell in sheet[1]:
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill('solid', fgColor='243C39')
        sheet.column_dimensions[cell.column_letter].width = 24
    sheet.freeze_panes = 'A2'
    sheet.auto_filter.ref = sheet.dimensions
    output = BytesIO()
    book.save(output)
    book.close()
    return output.getvalue()


def parse_workbook(stream):
    # Check inflated ZIP size before the XML parser reads spreadsheet content.
    try:
        with ZipFile(stream) as archive:
            if sum(i.file_size for i in archive.infolist()) > 40 * 1024 * 1024:
                raise ValidationError('Uncompressed workbook exceeds 40 MB.')
        stream.seek(0)
        book = load_workbook(stream, read_only=True, data_only=False)
    except ValidationError:
        raise
    except Exception as exc:
        raise ValidationError('Not a valid .xlsx workbook.') from exc
    try:
        if len(book.worksheets) != 1:
            raise ValidationError('Use a workbook with exactly one worksheet.')
        sheet = book.active
        if sheet.max_column and sheet.max_column > 245:
            raise ValidationError('Too many columns (maximum 245). Use the template.')
        if sheet.max_row and sheet.max_row > 1001:
            raise ValidationError('Import supports up to 1000 data rows.')
        rows = sheet.iter_rows()
        first = next(rows, ())
        headers = [normalize_header(str(c.value).strip()) if c.value is not None else '' for c in first]
        if len(headers) > 245 or not headers or 'Name' not in headers:
            raise ValidationError('Missing Name column or more than 245 columns. Download the template.')
        if len(headers) != len(set(headers)) or '' in headers:
            raise ValidationError('Headers must not be duplicate or empty.')
        columns = []
        reverse = {v: k for k, v in TYPES.items()}
        for h in headers:
            if h in BASE:
                continue
            match = PATTERN.fullmatch(h)
            if not match or int(match[2]) > 30:
                raise ValidationError(f'Unsupported column: {h}. Use the template format.')
            if not match[3]:
                columns.append((h, reverse[match[1]]))
            elif h[:-5] not in headers:
                raise ValidationError(f'{h} is missing its value column.')
        contacts = []
        for number, row in enumerate(rows, 2):
            if number > 1001:
                raise ValidationError('Import supports up to 1000 data rows.')
            if all(c.value is None for c in row):
                continue
            if any(c.data_type in {'f', 'e'} for c in row):
                raise ValidationError(f'Row {number}: formulas and error cells are not supported. Use text values.')
            data = {h: '' if c.value is None else str(c.value) for h, c in zip(headers, row)}
            favorite = data.get('Favorite', '').strip().lower()
            if favorite not in {'', 'yes', 'no', '是', '否', 'true', 'false', '1', '0'}:
                raise ValidationError(f'Row {number}: Favorite must be Yes or No.')
            methods = []
            for h, kind in columns:
                value, label = data.get(h, ''), data.get(h + 'Label', '')
                if value.strip():
                    methods.append(dict(type=kind, value=value, label=label))
                elif label.strip():
                    raise ValidationError(f'Row {number}: {h} has a label but no value.')
            try:
                contacts.append(validate_contact(dict(name=data.get('Name', ''), company=data.get('Company', ''),
                    group=data.get('Group', ''), notes=data.get('Notes', ''),
                    favorite=favorite in {'yes', '是', 'true', '1'}, methods=methods)))
            except ValidationError as exc:
                raise ValidationError(f'Row {number}: {exc}') from exc
        return contacts
    except ValidationError:
        raise
    except Exception as exc:
        raise ValidationError('Unable to read worksheet. Use a complete, undamaged template.') from exc
    finally:
        book.close()
