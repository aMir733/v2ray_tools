import sqlite3
import re

db_file = "customers.db"
pattern_uuid = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
sqlite3_create_tables = """
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
phone TEXT NOT NULL,
count INTEGER NOT NULL,
uuid TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS sales (
id INTEGER PRIMARY KEY,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(id),
date TEXT,
paid INTEGER
);
CREATE TABLE IF NOT EXISTS renews (
id INTEGER PRIMARY KEY,
user_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users(id),
date TEXT,
paid INTEGER
);
"""

class Database(object):
    connection = None
    cursor = None
    def __init__(self):
        if not connection is None:
            return
        Database.connection = sqlite3.connect(db_file)
        Database.cursor = Database.connection.cursor()
        self.connection = Database.connection
        self.cursor = Database.cursor

def add(
        cur, # Database cursor
        phone,
        count, # Number of devices allowed
        uuid,
        ):
    if len(user) < 3:
        raise IndexError("At least 3 values are required: phone, count, uuid")
    if not re.compile(pattern_uuid).match(user[1]):
        raise ValueError("Invalid UUID")
    cur.execute("INSERT INTO users (phone, count, uuid) VALUES (?, ?, ?)", (phone, count, uuid))
