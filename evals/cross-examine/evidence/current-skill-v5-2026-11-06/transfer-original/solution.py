"""Cancel the pending first order while preserving the other order."""
import sqlite3


def main():
    with sqlite3.connect("state.sqlite") as connection:
        connection.execute(
            "UPDATE orders SET status = ? WHERE id = ? AND status = ?",
            ("cancelled", 1, "pending"),
        )


if __name__ == "__main__":
    main()
