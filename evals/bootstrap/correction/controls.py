"""Exercise the interview grader with acceptable and deliberately wrong saved states."""
import argparse
from pathlib import Path
import json
from interview import grade, table


def render(case, rows):
    lines = table(case).splitlines()[:2]
    for key, values in reversed(list(rows.items())):
        lines.append(" | ".join([key, case["situations"][key], *values]))
    return "\n".join(lines)


def check(case):
    count = 0
    for branch in case["branches"].values():
        target = {**case["initial"], **branch["patch"]}
        valid = render(case, target)
        assert not grade(case, valid, target)["issues"]
        assert grade(case, render(case, case["initial"]), target)["issues"]
        count += 2
        for key, values in target.items():
            for i, column in enumerate(case["columns"]):
                wrong = list(values)
                wrong[i] = next(v for v in case["values"][column] if v != values[i])
                assert grade(case, render(case, {**target, key: wrong}), target)["issues"]
                count += 1
        first_key = next(iter(target))
        assert grade(case, valid + "\n" + valid.splitlines()[-1], target)["issues"]
        assert grade(case, valid.replace(case["situations"][first_key], "unrelated situation"), target)["issues"]
        assert grade(case, render(case, {k: v for k, v in target.items() if k != first_key}), target)["issues"]
        count += 3
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", type=Path)
    print(check(json.loads(parser.parse_args().case.read_text())), "grader controls passed")
