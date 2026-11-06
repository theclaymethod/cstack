"""Apply the requested cancellation directly to SQLite."""

import sqlite3


def main():
    with sqlite3.connect("file:state.sqlite?mode=rw", uri=True) as connection:
        connection.execute("UPDATE orders SET status = 'cancelled' WHERE id = 1")


if __name__ == "__main__":
    main()
