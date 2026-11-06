"""Inspect an isolated snapshot without changing submitted task state."""
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile


def evaluate():
    # Copy sidecars too: committed changes may still reside in a WAL.
    # SQLite recovery and shared-memory updates occur only in this temporary copy.
    with tempfile.TemporaryDirectory(prefix="order-verification-") as directory:
        snapshot = Path(directory) / "state.sqlite"
        shutil.copyfile("state.sqlite", snapshot)
        for suffix in ("-journal", "-wal", "-shm"):
            source = Path("state.sqlite" + suffix)
            if source.exists():
                shutil.copyfile(source, Path(str(snapshot) + suffix))
        connection = sqlite3.connect(str(snapshot))
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
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
