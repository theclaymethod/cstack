"""Replay a scripted correction and grade the two saved Markdown tables."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


def save(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def table(case):
    cols = ["ID", "Situation", *case["columns"]]
    rows = [cols, ["---"] * len(cols)]
    for key, situation in case["situations"].items():
        rows.append([key, situation, *([""] * len(case["columns"]))])
    return "\n".join("| " + " | ".join(row) + " |" for row in rows) + "\n"


def grade(case, md, expected):
    seen = {}
    issues = []
    header = ["ID", "Situation", *case["columns"]]
    for line in md.splitlines():
        if "|" not in line:
            continue
        row = [s.strip().strip("`").strip() for s in line.strip().strip("|").split("|")]
        if row == header or all(not s.strip(" :-") for s in row):
            continue
        key = row[0]
        if key in seen or key not in expected or len(row) != len(header):
            issues.append(f"Unexpected, duplicate or malformed row: {line}")
            continue
        if row[1] != case["situations"][key]:
            issues.append(f"{key}: situation changed")
        seen[key] = row[2:]
    for key, target in expected.items():
        if seen.get(key) != target:
            issues.append(f"{key}: expected {target}, observed {seen.get(key)}")
    return {"rows": seen, "issues": issues}


def replay(case_path, skill_path, branch, out, model):
    case = json.loads(case_path.read_text())
    decision = case["branches"][branch]
    skill = skill_path.read_bytes()
    out.mkdir(parents=True, exist_ok=False)
    save(out / "manifest.json", {"model": model, "cli": subprocess.check_output(["codex", "--version"], text=True).strip(),
         "branch": branch, "case_sha256": sha(case_path.read_bytes()), "skill_sha256": sha(skill),
         "runner_sha256": sha(Path(__file__).read_bytes())})
    artifact = case["artifact"]
    allowed = json.dumps(case["values"])
    prompt = (f"Use the supplied {case['skill']} skill. We keep our existing {artifact} as a Markdown table. "
              f"Preserve its ID, Situation and column schema. Allowed cell values: {allowed}. "
              "Use open for an undecided outcome or its evidence, proposed for a decided check without a direct observation, "
              "and observed-conflict when the recorded outcome contradicts the current expectation. "
              "Put explanations and interview questions in chat. Edit the actual file. Work only in this directory.\n\n"
              + skill.decode() + "\n\nDeveloper:\n" + case["turn_one"])
    target = {**case["initial"], **decision["patch"]}
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        file = work / artifact
        file.write_text(table(case))
        thread = None
        for i, (message, expected) in enumerate([(prompt, case["initial"]), (decision["reply"], target)], 1):
            cmd = ["codex", "exec", "--ignore-user-config", "--sandbox", "workspace-write", "-m", model,
                   "-c", 'web_search="disabled"']
            if i == 2:
                cmd += ["resume", "--ignore-user-config"]
            cmd += ["--skip-git-repo-check", "--json", "-o", str(out / f"reply-{i}.md")]
            if i == 2:
                cmd += [thread]
            proc = subprocess.run([*cmd, "-"], input=message, text=True, cwd=work, capture_output=True, timeout=240)
            events = [json.loads(line) for line in proc.stdout.splitlines() if line.startswith("{")]
            if proc.returncode:
                raise RuntimeError(proc.stderr[-1200:] + str(events[-1:])[:600])
            ids = [e["thread_id"] for e in events if e.get("type") == "thread.started"]
            if not ids or (thread and ids[0] != thread):
                raise RuntimeError("Could not verify interview thread continuity")
            thread = ids[0]
            if not file.exists():
                raise RuntimeError("Expected artifact missing")
            md = file.read_text()
            (out / f"turn-{i}.md").write_text(md)
            results.append(grade(case, md, expected))
    before, after = [phase["rows"] for phase in results]
    changed = {k: [before.get(k), after.get(k)] for k in before.keys() | after.keys()
               if before.get(k) != after.get(k)}
    result = {"turns": results, "delta": changed, "pass": not any(r["issues"] for r in results)}
    save(out / "result.json", result)
    return result["pass"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("case", "skill", "out"):
        parser.add_argument("--" + key, type=Path, required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--model", default="gpt-6-astra")
    args = parser.parse_args()
    raise SystemExit(0 if replay(args.case.resolve(), args.skill.resolve(), args.branch,
                                  args.out.resolve(), args.model) else 1)
