from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.db import query_db, execute_db
from routes.auth import login_required, role_required

payment_methods_bp = Blueprint('payment_methods', __name__, url_prefix='/payment-methods')

@payment_methods_bp.route('/')
@login_required
@role_required('gerente')
def list_payment_methods():
    payment_methods = query_db('SELECT * FROM payment_methods ORDER BY name;')
    return render_template('payment_methods.html', payment_methods=payment_methods)

@payment_methods_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('gerente')
def new_payment_method():
    if request.method == 'POST':
        name = request.form['name'].strip()
        active = 1 if request.form.get('active') else 0
        if not name:
            flash('Nome é obrigatório.', 'warning')
            return redirect(url_for('payment_methods.new_payment_method'))
        existing = query_db('SELECT id FROM payment_methods WHERE name = ?;', (name,), one=True)
        if existing:
            flash('Forma de pagamento já existe.', 'warning')
            return redirect(url_for('payment_methods.new_payment_method'))
        execute_db('INSERT INTO payment_methods (name, active) VALUES (?, ?);', (name, active))
        flash('Forma de pagamento cadastrada.', 'success')
        return redirect(url_for('payment_methods.list_payment_methods'))
    return render_template('payment_method_form.html', payment_method=None)

@payment_methods_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('gerente')
def edit_payment_method(id):
    payment_method = query_db('SELECT * FROM payment_methods WHERE id = ?;', (id,), one=True)
    if not payment_method:
        flash('Forma de pagamento não encontrada.', 'danger')
        return redirect(url_for('payment_methods.list_payment_methods'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        active = 1 if request.form.get('active') else 0
        if not name:
            flash('Nome é obrigatório.', 'warning')
            return redirect(url_for('payment_methods.edit_payment_method', id=id))
        existing = query_db('SELECT id FROM payment_methods WHERE name = ? AND id <> ?;', (name, id), one=True)
        if existing:
            flash('Outra forma de pagamento com esse nome já existe.', 'warning')
            return redirect(url_for('payment_methods.edit_payment_method', id=id))
        execute_db('UPDATE payment_methods SET name = ?, active = ? WHERE id = ?;', (name, active, id))
        flash('Forma de pagamento atualizada.', 'success')
        return redirect(url_for('payment_methods.list_payment_methods'))
    return render_template('payment_method_form.html', payment_method=payment_method)