import sqlite3
import re

# users sales renews
sql_create_projects_table = """
CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY,
phone text NOT NULL,
count int,
uuid text PRIMARY KEY,
);
CREATE TABLE IF NOT EXISTS sales (
id integer PRIMARY KEY,
user_id FOREIGN KEY
);
"""

pattern_uuid = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
def add(
        cur, # Database cursor
        phone,
        uuid,
        count, # Number of devices allowed
        ):
    if len(user) < 3:
        raise IndexError("At least 3 values are required: username, uuid, count")
    if not re.compile(pattern_uuid).match(user[1]):
        raise ValueError("Invalid UUID")
    cur.execute("INSERT INTO users VALUES ( ? , ? , ? )", )
