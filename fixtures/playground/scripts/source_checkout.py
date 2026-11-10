"""Resolve the owning C Stack checkout for fixtures and generated workspaces."""

import json
from pathlib import Path


def locate(explicit, project):
    project = Path(project).resolve()
    if explicit is not None:
        candidates = [Path(explicit).resolve()]
    else:
        metadata = project / '.cstack-source.json'
        candidates = ([Path(json.loads(metadata.read_text())['source']).resolve()] if metadata.exists() else [])
        candidates.extend(project.parents)
        candidates.append(project.parent / 'cstack')
    for candidate in candidates:
        manifest = candidate / 'plugin.json'
        if manifest.is_file() and json.loads(manifest.read_text()).get('name') == 'cstack' and (candidate / 'skills/hill-climb/SKILL.md').is_file():
            return candidate
    raise SystemExit('Use --source with a C Stack checkout')
