import os
import sqlite3
from models.db import DATABASE_SCHEMA

if __name__ == '__main__':
    db_path = os.path.join(os.path.dirname(__file__), 'eletrotech.db')
    if os.path.exists(db_path):
        print('Banco já existe:', db_path)
    else:
        with sqlite3.connect(db_path) as conn:
            with open(DATABASE_SCHEMA, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        print('Banco criado em:', db_path)
