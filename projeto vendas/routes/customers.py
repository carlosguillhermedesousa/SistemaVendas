from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.db import query_db, execute_db
from models.helpers import validate_cpf_cnpj, validate_cpf, validate_cnpj
from routes.auth import login_required, role_required

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customers_bp.route('/search')
@login_required
@role_required('gerente', 'vendedor')
def search_customers():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
    customers = query_db(
        'SELECT id, name, cpf_cnpj, email, status FROM customers WHERE name LIKE ? OR cpf_cnpj LIKE ? OR email LIKE ? ORDER BY name LIMIT 10;',
        (f'%{q}%', f'%{q}%', f'%{q}%')
    )
    return jsonify([dict(c) for c in customers])

@customers_bp.route('/')
@login_required
@role_required('gerente', 'vendedor')
def list_customers():
    query = request.args.get('q', '').strip()
    base = 'SELECT * FROM customers'
    params = ()
    if query:
        base += ' WHERE name LIKE ? OR cpf_cnpj LIKE ? OR email LIKE ?'
        wildcard = f'%{query}%'
        params = (wildcard, wildcard, wildcard)
    customers = query_db(base + ' ORDER BY name; ', params)
    return render_template('customers.html', customers=customers, query=query)

@customers_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('gerente', 'vendedor')
def new_customer():
    if request.method == 'POST':
        name = request.form['name'].strip()
        cpf_cnpj = request.form['cpf_cnpj'].strip()
        customer_type = request.form['customer_type']
        gender = request.form.get('gender', '').strip()
        email = request.form['email'].strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        status = request.form['status']
        if not (name and cpf_cnpj and email and customer_type):
            flash('Preencha todos os campos obrigatórios.', 'warning')
            return redirect(url_for('customers.new_customer'))
        if customer_type == 'Pessoa Física' and not validate_cpf(cpf_cnpj):
            flash('CPF inválido para pessoa física.', 'warning')
            return redirect(url_for('customers.new_customer'))
        if customer_type == 'Pessoa Jurídica' and not validate_cnpj(cpf_cnpj):
            flash('CNPJ inválido para pessoa jurídica.', 'warning')
            return redirect(url_for('customers.new_customer'))
        if not validate_cpf_cnpj(cpf_cnpj):
            flash('CPF/CNPJ inválido.', 'warning')
            return redirect(url_for('customers.new_customer'))
        existing = query_db('SELECT id FROM customers WHERE cpf_cnpj = ? OR email = ?;', (cpf_cnpj, email), one=True)
        if existing:
            flash('Cliente com o mesmo CPF/CNPJ ou email já existe.', 'warning')
            return redirect(url_for('customers.new_customer'))
        execute_db(
            'INSERT INTO customers (name, cpf_cnpj, customer_type, gender, email, phone, address, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
            (name, cpf_cnpj, customer_type, gender, email, phone, address, status)
        )
        flash('Cliente cadastrado com sucesso.', 'success')
        return redirect(url_for('customers.list_customers'))
    return render_template('customer_form.html', customer=None)

@customers_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('gerente', 'vendedor')
def edit_customer(id):
    customer = query_db('SELECT * FROM customers WHERE id = ?;', (id,), one=True)
    if not customer:
        flash('Cliente não encontrado.', 'danger')
        return redirect(url_for('customers.list_customers'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        cpf_cnpj = request.form['cpf_cnpj'].strip()
        customer_type = request.form['customer_type']
        gender = request.form.get('gender', '').strip()
        email = request.form['email'].strip()
        phone = request.form.get('phone', '').strip()
        address = request.form.get('address', '').strip()
        status = request.form['status']
        if not (name and cpf_cnpj and email and customer_type):
            flash('Preencha todos os campos obrigatórios.', 'warning')
            return redirect(url_for('customers.edit_customer', id=id))
        if customer_type == 'Pessoa Física' and not validate_cpf(cpf_cnpj):
            flash('CPF inválido para pessoa física.', 'warning')
            return redirect(url_for('customers.edit_customer', id=id))
        if customer_type == 'Pessoa Jurídica' and not validate_cnpj(cpf_cnpj):
            flash('CNPJ inválido para pessoa jurídica.', 'warning')
            return redirect(url_for('customers.edit_customer', id=id))
        if not validate_cpf_cnpj(cpf_cnpj):
            flash('CPF/CNPJ inválido.', 'warning')
            return redirect(url_for('customers.edit_customer', id=id))
        existing = query_db(
            'SELECT id FROM customers WHERE (cpf_cnpj = ? OR email = ?) AND id <> ?;', (cpf_cnpj, email, id), one=True
        )
        if existing:
            flash('Outro cliente com o mesmo CPF/CNPJ ou email já existe.', 'warning')
            return redirect(url_for('customers.edit_customer', id=id))
        execute_db(
            'UPDATE customers SET name = ?, cpf_cnpj = ?, customer_type = ?, gender = ?, email = ?, phone = ?, address = ?, status = ? WHERE id = ?;', 
            (name, cpf_cnpj, customer_type, gender, email, phone, address, status, id)
        )
        flash('Cliente atualizado com sucesso.', 'success')
        return redirect(url_for('customers.list_customers'))
    purchases = query_db(
        'SELECT s.id, s.datetime, s.total_amount FROM sales s WHERE s.customer_id = ? ORDER BY s.datetime DESC LIMIT 5;', 
        (id,)
    )
    return render_template('customer_form.html', customer=customer, purchases=purchases)
