"""Commit the requested cancellation without changing other orders."""
import sqlite3


def main():
    connection = sqlite3.connect("file:state.sqlite?mode=rw", uri=True)
    try:
        with connection:
            connection.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                ("cancelled", 1),
            )
    finally:
        connection.close()


if __name__ == "__main__":
    main()
