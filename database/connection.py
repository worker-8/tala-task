import json
import sqlite3
import os

path = os.path.dirname(os.path.abspath(__file__))
# TODO: move to toml config them
db = os.path.join(path, 'db.db')


def create_sqlite3_conn():
    sqlite3.register_adapter(dict, lambda x: json.dumps(x))
    sqlite3.register_converter("json", lambda x: json.loads(x))

    connection = sqlite3.connect(
        db, detect_types=sqlite3.PARSE_DECLTYPES, timeout=20)
    connection.row_factory = sqlite3.Row

    return connection
