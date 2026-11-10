"""Validate local calibration mechanics without contacting a model provider."""
import argparse
import json
from pathlib import Path
from .workflow import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.out)
    print(json.dumps({key: result[key] for key in ['status', 'native_source_executions', 'fixture_judge_processes',
          'source_families', 'final_refit_blocked', 'provider_calls', 'live_backend_status', 'promotion']}, indent=2))


if __name__ == '__main__':
    main()
