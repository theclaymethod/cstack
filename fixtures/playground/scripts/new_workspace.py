"""Materialize this fixture with current C Stack skills in a new local workspace."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from source_checkout import locate

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--source', type=Path)
    args = parser.parse_args()
    source = locate(args.source, ROOT)
    output = args.out.resolve()
    if output.exists() or output.is_symlink():
        raise SystemExit('Choose a new workspace directory; existing work is preserved')
    if output == ROOT or ROOT in output.parents:
        raise SystemExit('Create workspaces outside the canonical fixture directory')
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix='.playground-', dir=output.parent))
    try:
        staged = temporary / 'workspace'
        shutil.copytree(ROOT, staged, symlinks=True,
                        ignore=shutil.ignore_patterns('.git', '.agents', '.claude', '.cursor',
                                                     'cstack-skills.lock.json', '.cstack-source.json',
                                                     'eval-runs', '.venv', '__pycache__', '*.pyc', '.DS_Store'))
        (staged / '.cstack-source.json').write_text(json.dumps({'source': str(source)}, indent=2) + '\n')
        install = subprocess.run([sys.executable, str(staged / 'scripts/sync_skills.py'), '--source', str(source)],
                                 text=True, capture_output=True)
        if install.returncode:
            raise SystemExit(install.stderr or install.stdout)
        initialized = subprocess.run(['git', 'init', '-b', 'main'], cwd=staged, text=True, capture_output=True)
        if initialized.returncode:
            raise SystemExit(initialized.stderr)
        if output.exists():
            raise SystemExit('Workspace appeared during preparation; refusing overwrite')
        os.rename(staged, output)
    finally:
        shutil.rmtree(temporary)
    print(json.dumps({'workspace': str(output), 'source': str(source), 'skills': json.loads(install.stdout)['installed'],
                      'git': 'local repository initialized; no remote or commit'}, indent=2))


if __name__ == '__main__':
    main()
