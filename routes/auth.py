import sqlite3
from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import query_db, execute_db, get_db
from models.helpers import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped_view(**kwargs):
            if 'role' not in session or session['role'] not in roles:
                flash('Acesso negado: permissão insuficiente.', 'danger')
                return redirect(url_for('dashboard.index'))
            return view(**kwargs)
        return wrapped_view
    return decorator

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        user = query_db('SELECT * FROM users WHERE username = ?;', (username,), one=True)
        if user and verify_password(password, user['password']):
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['role'] = user['role']
            flash('Bem-vindo(a), ' + user['name'], 'success')
            return redirect(url_for('dashboard.index'))
        session.clear()
        flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Você saiu do sistema.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
@role_required('gerente')
def register():
    if request.method == 'POST':
        name = request.form['name'].strip()
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form['role']
        if not (name and username and password and role):
            flash('Preencha todos os campos.', 'warning')
            return redirect(url_for('auth.register'))
        existing_user = query_db('SELECT id FROM users WHERE username = ?;', (username,), one=True)
        if existing_user:
            flash('Nome de usuário já cadastrado.', 'warning')
            return redirect(url_for('auth.register'))
        hashed = hash_password(password)
        execute_db(
            'INSERT INTO users (name, username, password, role) VALUES (?, ?, ?, ?);',
            (name, username, hashed, role)
        )
        flash('Usuário cadastrado com sucesso.', 'success')
        return redirect(url_for('auth.register'))
    users = query_db('SELECT id, name, username, role FROM users ORDER BY role, name;')
    return render_template(
        'register.html',
        users=users,
        form_action=url_for('auth.register'),
        form_title='Novo usuário',
        submit_label='Cadastrar'
    )

@auth_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('gerente')
def edit_user(id):
    user = query_db('SELECT * FROM users WHERE id = ?;', (id,), one=True)
    if not user:
        flash('Usuário não encontrado.', 'danger')
        return redirect(url_for('auth.register'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        username = request.form['username'].strip()
        password = request.form.get('password', '').strip()
        role = request.form['role']
        if not (name and username and role):
            flash('Preencha todos os campos.', 'warning')
            return redirect(url_for('auth.edit_user', id=id))
        existing_user = query_db('SELECT id FROM users WHERE username = ? AND id <> ?;', (username, id), one=True)
        if existing_user:
            flash('Nome de usuário já cadastrado.', 'warning')
            return redirect(url_for('auth.edit_user', id=id))
        if password:
            hashed = hash_password(password)
            execute_db(
                'UPDATE users SET name = ?, username = ?, password = ?, role = ? WHERE id = ?;', 
                (name, username, hashed, role, id)
            )
        else:
            execute_db(
                'UPDATE users SET name = ?, username = ?, role = ? WHERE id = ?;', 
                (name, username, role, id)
            )
        flash('Usuário atualizado com sucesso.', 'success')
        return redirect(url_for('auth.register'))
    users = query_db('SELECT id, name, username, role FROM users ORDER BY role, name;')
    return render_template(
        'register.html',
        users=users,
        edit_user=user,
        form_action=url_for('auth.edit_user', id=id),
        form_title='Editar usuário',
        submit_label='Salvar alterações'
    )

@auth_bp.app_context_processor
def inject_user():
    return {'current_user': session}
