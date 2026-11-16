"""Build two disjoint source packages for the agreed feature ownership."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT.parent / 'team-handoff'
EXCLUDED = {'.git', '.venv', '__pycache__', '.pytest_cache', 'instance'}
B_FILES = {
    'addressbook/excel.py',
    'addressbook/excel_routes.py',
    'addressbook/static/excel.js',
    'tests/test_excel.py',
    'docs/EXCEL_FORMAT.md',
}


def build():
    OUTPUT.mkdir(exist_ok=True)
    files = {
        path.relative_to(ROOT).as_posix(): path for path in ROOT.rglob('*')
        if path.is_file() and not EXCLUDED.intersection(path.relative_to(ROOT).parts)
        and path.suffix not in {'.sqlite3', '.pyc', '.log'}
    }
    assert B_FILES <= files.keys(), 'A required B file is missing.'
    groups = {'A': set(files) - B_FILES, 'B': B_FILES}
    assert groups['A'].isdisjoint(groups['B'])
    assert groups['A'] | groups['B'] == files.keys()
    manifest = {}
    for owner, names in groups.items():
        archive_path = OUTPUT / f'address-book-{owner}.zip'
        with ZipFile(archive_path, 'w', ZIP_DEFLATED) as archive:
            for name in sorted(names):
                archive.write(files[name], name)
                manifest[name] = {'owner': owner, 'sha256': hashlib.sha256(files[name].read_bytes()).hexdigest()}
        with ZipFile(archive_path) as archive:
            assert archive.testzip() is None
        print(f'{owner}: {len(names)} files -> {archive_path}')
    (OUTPUT / 'file-ownership.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    (OUTPUT / 'README.md').write_text((ROOT / 'docs/GITHUB_HANDOFF.md').read_text(encoding='utf-8').replace('[DEPLOYMENT.md](DEPLOYMENT.md)', '`docs/DEPLOYMENT.md`（合并后的仓库内）'), encoding='utf-8')


if __name__ == '__main__':
    build()
