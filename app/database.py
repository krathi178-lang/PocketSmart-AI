import sqlite3
from contextlib import contextmanager
from .config import DATA_DIR
DB_PATH=DATA_DIR/'pocketsmart.db'
SCHEMA='''
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,password_hash TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS recommendations(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,planner_type TEXT NOT NULL,request_json TEXT NOT NULL,response_json TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id));
'''
def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.executescript(SCHEMA)
        cols={r[1] for r in c.execute('PRAGMA table_info(recommendations)').fetchall()}
        required={'user_id','planner_type','request_json','response_json'}
        if not required.issubset(cols):
            c.execute('DROP TABLE IF EXISTS recommendations')
            c.execute('''CREATE TABLE recommendations(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER NOT NULL,planner_type TEXT NOT NULL,request_json TEXT NOT NULL,response_json TEXT NOT NULL,created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,FOREIGN KEY(user_id) REFERENCES users(id))''')
        c.commit()
@contextmanager
def get_db():
    c=sqlite3.connect(DB_PATH); c.row_factory=sqlite3.Row
    try: yield c; c.commit()
    finally: c.close()
