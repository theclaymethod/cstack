import sqlite3
with sqlite3.connect('state.sqlite') as db:
    db.execute("UPDATE customers SET address='New Lane' WHERE id=1")
