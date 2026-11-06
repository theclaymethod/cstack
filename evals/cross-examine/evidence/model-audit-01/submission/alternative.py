import sqlite3

with sqlite3.connect("state.sqlite") as db:
    db.execute("UPDATE customers SET address = ? WHERE id = ?", ("New Lane", 1))
