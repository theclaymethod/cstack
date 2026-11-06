"""Read task state independently of agent-authored output files."""
import json
import sqlite3
import sys
import tempfile
from pathlib import Path


def evaluate():
    # Snapshot the database and any WAL into an isolated directory. SQLite may
    # create shared-memory files while opening a WAL database; those writes
    # must never affect the submitted state. Verification runs after the agent
    # has finished, with no concurrent database writer.
    with tempfile.TemporaryDirectory(prefix="order-verification-") as temporary:
        snapshot = Path(temporary) / "state.sqlite"
        snapshot.write_bytes(Path("state.sqlite").read_bytes())
        for suffix in ("-wal", "-journal"):
            source = Path("state.sqlite" + suffix)
            if source.exists():
                Path(str(snapshot) + suffix).write_bytes(source.read_bytes())
        connection = sqlite3.connect(snapshot.as_uri() + "?mode=ro", uri=True)
        try:
            connection.execute("PRAGMA query_only = ON")
            rows = connection.execute(
                "SELECT id, status FROM orders ORDER BY id"
            ).fetchall()
            return rows == [(1, "cancelled"), (2, "shipped")]
        finally:
            connection.close()


def main():
    try:
        passed = bool(evaluate())
    except Exception:
        passed = False
    print(json.dumps({"passed": passed}))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
