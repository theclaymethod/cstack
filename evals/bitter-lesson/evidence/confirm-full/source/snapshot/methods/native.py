"""Use the fixture's existing runner and keep every execution recoverable."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location('methods_native_evaluate', ROOT / 'evaluate.py')
evaluate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(evaluate)


def write(path, value):
    path = Path(path)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')


def jsonl(path, values):
    Path(path).write_text(''.join(json.dumps(value, sort_keys=True) + '\n' for value in values))


def read_rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


class Runs:
    def __init__(self, directory, limit=400):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=False)
        self.limit = limit
        self.reserved = 0
        self.calls = []

    def run(self, label, candidate, cases):
        case_file = self.directory / (label + '.jsonl')
        output = self.directory / label
        if (not label or Path(label).name != label or label in {call['label'] for call in self.calls}
                or case_file.exists() or case_file.is_symlink() or output.exists() or output.is_symlink()):
            raise ValueError('Choose an unused single-component run label; prior evidence is preserved')
        if self.reserved + len(cases) > self.limit:
            raise RuntimeError('Native execution budget exhausted')
        self.reserved += len(cases)
        jsonl(case_file, cases)
        # Reservation persists even if execution raises; a retry needs a new label/reservation.
        call = {'label': label, 'candidate': str(candidate), 'cases': str(case_file),
                'reserved': len(cases), 'status': 'pending'}
        self.calls.append(call)
        self.save()
        summary = evaluate.run_suite(candidate, 'all', output, case_file)
        evaluate.checked_run(output)
        call.update(status='complete', executed=summary['executed_count'], counts=summary['counts'])
        self.save()
        return read_rows(output / 'traces.jsonl')

    def save(self):
        write(self.directory / 'executions.json', {'limit': self.limit, 'reserved': self.reserved,
              'actual_completed': sum(c.get('executed', 0) for c in self.calls), 'calls': self.calls})
