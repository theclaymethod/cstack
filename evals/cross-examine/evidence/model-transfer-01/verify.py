"""Judge the database itself without writing to task state."""

import json
import sqlite3
import sys


def passed():
    connection = None
    try:
        connection = sqlite3.connect(
            "file:state.sqlite?mode=ro", uri=True, timeout=1
        )
        rows = connection.execute(
            "SELECT id, status FROM orders ORDER BY id"
        ).fetchall()
        return rows == [(1, "cancelled"), (2, "shipped")]
    except (sqlite3.Error, OSError):
        return False
    finally:
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    success = passed()
    print(json.dumps({"passed": success}))
    sys.exit(0 if success else 1)
