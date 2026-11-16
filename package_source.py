"""Create a reproducible source handoff archive without databases or caches."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent
DESTINATION = ROOT.parent / 'address-book-source.zip'
EXCLUDED = {'.git', '.venv', '__pycache__', '.pytest_cache', 'instance'}

if __name__ == '__main__':
    with ZipFile(DESTINATION, 'w', ZIP_DEFLATED) as archive:
        for file in sorted(ROOT.rglob('*')):
            relative = file.relative_to(ROOT)
            if file.is_file() and not any(part in EXCLUDED for part in relative.parts):
                if file.suffix not in {'.sqlite3', '.pyc', '.log'}:
                    archive.write(file, Path('address-book') / relative)
    print(DESTINATION)
