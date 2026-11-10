"""Copy the sibling C Stack pack locally while preserving modified installations."""

import argparse
import hashlib
import json
from pathlib import Path
import shutil

from source_checkout import locate

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / 'cstack-skills.lock.json'


def files(folder):
    return {str(p.relative_to(folder)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(folder.rglob('*')) if p.is_file()
            and '__pycache__' not in p.parts and p.name != '.DS_Store'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    previous = json.loads(LOCK.read_text()) if LOCK.exists() else {'skills': {}}
    installed = ROOT / '.agents/skills'
    for name, hashes in previous['skills'].items():
        if files(installed / name) != hashes:
            raise SystemExit('Installed skill changed; preserve your edits before syncing: ' + name)
    if args.check:
        if not previous['skills']:
            raise SystemExit('No installed C Stack skills; run sync with --source first')
        print(json.dumps({'verified': sorted(previous['skills'])}, indent=2))
        return
    source = locate(args.source, ROOT)
    names = sorted(p.parent.name for p in (source / 'skills').glob('*/SKILL.md'))
    if not names or not (source / 'plugin.json').is_file():
        raise SystemExit('Source is not a C Stack checkout')
    for name in names:
        destination = installed / name
        if destination.exists() and name not in previous['skills']:
            raise SystemExit('Unmanaged installed skill exists; refusing overwrite: ' + name)
    for agent in ['.claude', '.cursor']:
        for name in names:
            link = ROOT / agent / 'skills' / name
            wanted = Path('../../.agents/skills') / name
            if link.is_symlink():
                if link.readlink() != wanted:
                    raise SystemExit('Existing skill link points elsewhere: ' + str(link))
            elif link.exists():
                raise SystemExit('Existing skill path is not a managed link: ' + str(link))
    for name in names:
        destination = installed / name
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source / 'skills' / name, destination,
                        ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.DS_Store'))
        for agent in ['.claude', '.cursor']:
            link = ROOT / agent / 'skills' / name
            link.parent.mkdir(parents=True, exist_ok=True)
            if not link.is_symlink():
                link.symlink_to(Path('../../.agents/skills') / name)
    lock = {'source': 'theclaymethod/cstack', 'version': json.loads((source / 'plugin.json').read_text())['version'],
            'skills': {name: files(installed / name) for name in names}}
    LOCK.write_text(json.dumps(lock, indent=2) + '\n')
    print(json.dumps({'installed': names, 'version': lock['version']}, indent=2))


if __name__ == '__main__':
    main()
