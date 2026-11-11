"""Run offline ablation and model-migration mechanics with no provider calls."""
import argparse
import json
from pathlib import Path
from .demo import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = run(args.out)
    print(json.dumps({key: result[key] for key in ('status', 'native_case_executions',
          'confirmation_case_executions', 'burden', 'provider_calls', 'paid_calls', 'promotion')}, indent=2))


if __name__ == '__main__':
    main()
