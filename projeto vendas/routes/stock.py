from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import query_db, execute_db
from routes.auth import login_required, role_required

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

@stock_bp.route('/entry', methods=['GET', 'POST'])
@login_required
@role_required('gerente', 'estoquista')
def entry():
    products = query_db('SELECT * FROM products ORDER BY name;')
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            flash('Quantidade deve ser um número inteiro positivo.', 'warning')
            return redirect(url_for('stock.entry'))
        product = query_db('SELECT * FROM products WHERE id = ?;', (product_id,), one=True)
        if not product:
            flash('Produto não encontrado.', 'danger')
            return redirect(url_for('stock.entry'))
        execute_db('UPDATE products SET stock = stock + ? WHERE id = ?;', (quantity, product_id))
        execute_db(
            'INSERT INTO stock_movements (product_id, user_id, datetime, type, quantity, description) VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?);',
            (product_id, session['user_id'], 'Entrada', quantity, 'Entrada de estoque manual')
        )
        flash('Estoque atualizado com sucesso.', 'success')
        return redirect(url_for('stock.entry'))
    return render_template('stock_entry.html', products=products)

@stock_bp.route('/exit', methods=['GET', 'POST'])
@login_required
@role_required('gerente', 'estoquista')
def exit_stock():
    products = query_db('SELECT * FROM products ORDER BY name;')
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        description = request.form.get('description', '').strip()
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except (ValueError, TypeError):
            flash('Quantidade deve ser um número inteiro positivo.', 'warning')
            return redirect(url_for('stock.exit_stock'))
        product = query_db('SELECT * FROM products WHERE id = ?;', (product_id,), one=True)
        if not product:
            flash('Produto não encontrado.', 'danger')
            return redirect(url_for('stock.exit_stock'))
        if quantity > product['stock']:
            flash('Quantidade maior que o estoque disponível.', 'danger')
            return redirect(url_for('stock.exit_stock'))
        execute_db('UPDATE products SET stock = stock - ? WHERE id = ?;', (quantity, product_id))
        execute_db(
            'INSERT INTO stock_movements (product_id, user_id, datetime, type, quantity, description) VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?);',
            (product_id, session['user_id'], 'Saída', quantity, description or 'Saída de estoque manual')
        )
        flash('Estoque atualizado com sucesso.', 'success')
        return redirect(url_for('stock.exit_stock'))
    return render_template('stock_exit.html', products=products)

@stock_bp.route('/movements')
@login_required
@role_required('gerente', 'estoquista')
def movements():
    movements = query_db(
        'SELECT m.*, p.name AS product_name, u.username AS user_name FROM stock_movements m '
        'LEFT JOIN products p ON p.id = m.product_id LEFT JOIN users u ON u.id = m.user_id '
        'ORDER BY m.datetime DESC LIMIT 100;'
    )
    return render_template('stock_movements.html', movements=movements)
