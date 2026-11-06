"""Prepare a fresh attempt. Run only as the operator."""
from pathlib import Path
import sqlite3


def main():
    for name in (
        "state.sqlite", "state.sqlite-wal", "state.sqlite-shm",
        "state.sqlite-journal", "result.json", "audit.json",
    ):
        Path(name).unlink(missing_ok=True)
    connection = sqlite3.connect("state.sqlite")
    try:
        with connection:
            connection.execute(
                "CREATE TABLE orders(id INTEGER PRIMARY KEY, status TEXT NOT NULL)"
            )
            connection.executemany(
                "INSERT INTO orders(id, status) VALUES (?, ?)",
                [(1, "pending"), (2, "shipped")],
            )
    finally:
        connection.close()


if __name__ == "__main__":
    main()
