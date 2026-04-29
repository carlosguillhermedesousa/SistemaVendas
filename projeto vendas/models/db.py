import os
import sqlite3
from flask import g

DATABASE_SCHEMA = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(
            os.path.join(os.path.dirname(__file__), '..', 'database', 'eletrotech.db')
        )
        db.row_factory = sqlite3.Row
    return db


def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def _ensure_customer_columns(conn):
    columns = [row[1] for row in conn.execute('PRAGMA table_info(customers);').fetchall()]
    if 'customer_type' not in columns:
        conn.execute("ALTER TABLE customers ADD COLUMN customer_type TEXT NOT NULL DEFAULT 'Pessoa Física';")
    if 'gender' not in columns:
        conn.execute("ALTER TABLE customers ADD COLUMN gender TEXT;")


def init_db(app):
    db_path = app.config['DATABASE']
    db_needs_creation = not os.path.exists(db_path)
    with app.app_context():
        from models.helpers import hash_password
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        if db_needs_creation:
            with open(DATABASE_SCHEMA, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
            conn.execute(
                'INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?);',
                ('Gerente Admin', 'admin', hash_password('admin123'), 'gerente')
            )
            conn.execute(
                'INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?);',
                ('Vendedor Padrão', 'vendedor', hash_password('vendedor123'), 'vendedor')
            )
            conn.execute(
                'INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?);',
                ('Estoquista Padrão', 'estoquista', hash_password('estoquista123'), 'estoquista')
            )
            conn.execute(
                'INSERT INTO customers (name, cpf_cnpj, customer_type, gender, email, status) VALUES (?, ?, ?, ?, ?, ?);',
                ('Eletro Comercial', '12345678909', 'Pessoa Jurídica', 'Outro', 'compras@eletrotech.com.br', 'Ativo')
            )
            conn.execute(
                'INSERT INTO products (barcode, name, category, cost_price, margin, sale_price, stock, min_stock) VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
                ('7891234567895', 'Multímetro Digital', 'Ferramentas', 85.00, 30.0, 110.50, 15, 5)
            )
            conn.execute('INSERT INTO payment_methods (name, active) VALUES (?, ?);', ('Dinheiro', 1))
            conn.execute('INSERT INTO payment_methods (name, active) VALUES (?, ?);', ('Cartão', 1))
            conn.execute('INSERT INTO payment_methods (name, active) VALUES (?, ?);', ('PIX', 1))
        else:
            _ensure_customer_columns(conn)
            default_users = [
                ('Gerente Admin', 'admin', 'admin123', 'gerente'),
                ('Vendedor Padrão', 'vendedor', 'vendedor123', 'vendedor'),
                ('Estoquista Padrão', 'estoquista', 'estoquista123', 'estoquista'),
            ]
            for name, username, password, role in default_users:
                exists = conn.execute('SELECT id FROM users WHERE username = ?;', (username,)).fetchone()
                if not exists:
                    conn.execute(
                        'INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?);',
                        (name, username, hash_password(password), role)
                    )
        conn.commit()
        conn.close()
    app.teardown_appcontext(close_db)


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def execute_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    return cur.lastrowid
