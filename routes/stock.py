from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.db import query_db, execute_db
from routes.auth import login_required, role_required

stock_bp = Blueprint('stock', __name__, url_prefix='/stock')

@stock_bp.route('/entry', methods=['GET', 'POST'])
@login_required
@role_required('gerente', 'estoquista')
def entry():
    products = query_db('SELECT * FROM products ORDER BY name;')
    movements = query_db(
        'SELECT m.*, p.name AS product_name, u.username AS user_name '
        'FROM stock_movements m '
        'LEFT JOIN products p ON p.id = m.product_id '
        'LEFT JOIN users u ON u.id = m.user_id '
        'ORDER BY m.datetime DESC LIMIT 10;'
    )
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        movement_type = request.form.get('movement_type', 'Entrada')
        description = request.form.get('description', '').strip()
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
        if movement_type == 'Saída' and quantity > product['stock']:
            flash('Quantidade maior que o estoque disponível.', 'danger')
            return redirect(url_for('stock.entry'))
        if movement_type == 'Saída':
            execute_db('UPDATE products SET stock = stock - ? WHERE id = ?;', (quantity, product_id))
        else:
            execute_db('UPDATE products SET stock = stock + ? WHERE id = ?;', (quantity, product_id))
        execute_db(
            'INSERT INTO stock_movements (product_id, user_id, datetime, type, quantity, description) VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?);',
            (product_id, session['user_id'], movement_type, quantity, description or f'{movement_type} de estoque manual')
        )
        flash(f'Estoque atualizado com sucesso ({movement_type}).', 'success')
        return redirect(url_for('stock.entry'))
    return render_template('stock_entry.html', products=products, movements=movements)

@stock_bp.route('/exit')
@login_required
@role_required('gerente', 'estoquista')
def exit_stock():
    return redirect(url_for('stock.entry'))

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
