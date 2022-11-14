from re import compile as recompile
from json import load as jsonload, dump as jsondump

class Database(object):
    def __init__(self, db_path="customers.db"):
        import sqlite3
        sqlite3_create_tables = """CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY,
phone TEXT UNIQUE NOT NULL,
count INTEGER NOT NULL,
uuid TEXT UNIQUE NOT NULL,
disconnected INTEGER
);
CREATE TABLE IF NOT EXISTS sales (
id INTEGER PRIMARY KEY,
user_id INTEGER,
date TEXT,
paid INTEGER,
start INTEGER,
FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS deleted (
id INTEGER PRIMARY KEY,
user_id INTEGER,
phone TEXT,
count INTEGER,
uuid TEXT,
FOREIGN KEY(user_id) REFERENCES users(id)
);
"""
        Database.con = sqlite3.connect(db_path)
        Database.cur = Database.con.cursor()
        Database.cur.executescript(sqlite3_create_tables)

def make_config(
        clients, # List of clients to add to configuration: [(x,y,z),(a,b,c)]
        path, # Path to your configuration file
        dest="config_new.json", # Where to store the new configuration file
        ):
    if type(clients) != list:
        raise TypeError("Invalid type for clients. Only lists are acceptable")
    with open(path, "r") as f:
        js = jsonload(f)
    if not 'inbounds' in js:
        raise KeyError("Could not find the 'inbounds' entry in {} . If you're using the 'inbound' keyword please change it to 'inbounds'".format(path))
    passed = None
    for inbound in js['inbounds']:
        if inbound['protocol'] != 'vmess' and inbound['protocol'] != 'vless':
            continue
        default_client = inbound['settings']['clients'][0]
        if default_client['email'] != "v2ray_tools":
            continue
        passed = True
        max_digits = len(str(max(clients)[0]))
        for client in clients:
            inbound['settings']['clients'].append({
                **default_client,
                "id": client[3], # uuid
                "email": str(client[0]).zfill(max_digits), # email
            })
    if passed != True:
        raise ValueError("Could not find an appropriate inbound")
    with open(dest, "w") as f:
        jsondump(js, f)
    return dest

def add_user(
        db, # Database object
        phone,
        count, # Number of devices allowed
        uuid,
        ):
    pattern_uuid = r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$'
    if not recompile(pattern_uuid).match(uuid):
        raise ValueError("Invalid UUID")
    db.cur.execute("INSERT INTO users (phone, count, uuid) VALUES (?, ?, ?)", (phone, count, uuid))
    db.con.commit()

def get_user(
        db, # Database object
        query, # An array or a tuple: (column name, query)
        size=1,
        ):
    check_query(query)
    res = db.cur.execute("SELECT * FROM users WHERE {} LIKE ?".format(query[0]), (query[1],))
    if size == 0:
        return res.fetchall()
    return res.fetchmany(size=size)

def del_user(
        db, # Database object
        query, # An array or a tuple: (column name, query)
        ):
    check_query(query)
    res = get_user(db, query)
    if len(res) < 4:
        raise ValueError("Invalid number of columns received from get_user")
    if len(res) > 4:
        res = [i[:-1] for i in res]
    db.cur.execute("DELETE FROM users WHERE {} LIKE ? LIMIT 1".format(query[0]), (query[1],))
    db.cur.executemany("INSERT INTO deleted (user_id, phone, count, uuid) VALUES ( ?, ?, ?, ? )", res)
    db.con.commit()

def mod_user(
        db,
        query, # An array or a tuple: (column name, query)
        **kwargs, # columns to be changed
        ):
    check_query(query)
    if len(kwargs) < 1:
        raise IndexError("At least one kwarg is required for this function")
    set_string = []
    pattern_word = r'^[0-9A-Za-z]{,24}$'
    for kwarg in kwargs:
        if not recompile(pattern_word).match(kwarg):
            raise ValueError("No SQL Injection allowed")
        set_string.append("{} = ?".format(kwarg))
    res = db.cur.execute(
            "UPDATE users SET {} WHERE {} = ?".format(', '.join(set_string), query[0]),
            tuple(kwargs.values()) + (query[1],)
            )
    db.con.commit()
    return res

def check_query(query):
    pattern_word = r'^[0-9A-Za-z]{,24}$'
    if len(query) != 2:
        raise ValueError("Query needs to be a tuple containing the column name and the query")
    if not recompile(pattern_word).match(query[0]):
        raise ValueError("No SQL Injection allowed")
