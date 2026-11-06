"""Reconstruct an attempt from trusted fixture data."""

from pathlib import Path
import shutil
import sqlite3


def main():
    for name in (
        "state.sqlite", "state.sqlite-journal", "state.sqlite-wal",
        "state.sqlite-shm", "result.json", "audit.json",
    ):
        path = Path(name)
        if path.is_symlink() or path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
    with sqlite3.connect("state.sqlite") as connection:
        connection.execute(
            "CREATE TABLE orders(id INTEGER PRIMARY KEY, status TEXT NOT NULL)"
        )
        connection.executemany(
            "INSERT INTO orders(id, status) VALUES (?, ?)",
            [(1, "pending"), (2, "shipped")],
        )


if __name__ == "__main__":
    main()
