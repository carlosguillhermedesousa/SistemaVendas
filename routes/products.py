from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models.db import query_db, execute_db
from models.helpers import calculate_sale_price
from routes.auth import login_required, role_required

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/search')
@login_required
@role_required('gerente', 'estoquista')
def search_products():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
    products = query_db(
        'SELECT id, barcode, name, category, sale_price, stock FROM products WHERE barcode LIKE ? OR name LIKE ? OR category LIKE ? ORDER BY name LIMIT 10;',
        (f'%{q}%', f'%{q}%', f'%{q}%')
    )
    return jsonify([dict(p) for p in products])

@products_bp.route('/')
@login_required
@role_required('gerente', 'estoquista')
def list_products():
    query = request.args.get('q', '').strip()
    base = 'SELECT * FROM products'
    params = ()
    if query:
        base += ' WHERE barcode LIKE ? OR name LIKE ? OR category LIKE ?'
        wildcard = f'%{query}%'
        params = (wildcard, wildcard, wildcard)
    products = query_db(base + ' ORDER BY name;', params)
    return render_template('products.html', products=products, query=query)

@products_bp.route('/new', methods=['GET', 'POST'])
@login_required
@role_required('gerente', 'estoquista')
def new_product():
    if request.method == 'POST':
        barcode = request.form['barcode'].strip()
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        category = request.form['category'].strip()
        brand = request.form.get('brand', '').strip()
        cost_price = request.form['cost_price']
        margin = request.form['margin']
        min_stock = request.form['min_stock']
        unit = request.form.get('unit', 'UN').strip()
        if not (barcode and name and category and cost_price and margin and min_stock):
            flash('Preencha todos os campos obrigatórios.', 'warning')
            return redirect(url_for('products.new_product'))
        try:
            cost_price = float(cost_price)
            margin = float(margin)
            min_stock = int(min_stock)
        except ValueError:
            flash('Valores numéricos inválidos.', 'warning')
            return redirect(url_for('products.new_product'))
        existing = query_db('SELECT id FROM products WHERE barcode = ?;', (barcode,), one=True)
        if existing:
            flash('Código de barras já cadastrado.', 'warning')
            return redirect(url_for('products.new_product'))
        sale_price = calculate_sale_price(cost_price, margin)
        execute_db(
            'INSERT INTO products (barcode, name, description, category, brand, cost_price, margin, sale_price, stock, min_stock, unit) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?);',
            (barcode, name, description, category, brand, cost_price, margin, sale_price, min_stock, unit)
        )
        flash('Produto cadastrado com sucesso.', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('product_form.html', product=None)

@products_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@role_required('gerente', 'estoquista')
def edit_product(id):
    product = query_db('SELECT * FROM products WHERE id = ?;', (id,), one=True)
    if not product:
        flash('Produto não encontrado.', 'danger')
        return redirect(url_for('products.list_products'))
    if request.method == 'POST':
        barcode = request.form['barcode'].strip()
        name = request.form['name'].strip()
        description = request.form.get('description', '').strip()
        category = request.form['category'].strip()
        brand = request.form.get('brand', '').strip()
        cost_price = request.form['cost_price']
        margin = request.form['margin']
        min_stock = request.form['min_stock']
        unit = request.form.get('unit', 'UN').strip()
        if not (barcode and name and category and cost_price and margin and min_stock):
            flash('Preencha todos os campos obrigatórios.', 'warning')
            return redirect(url_for('products.edit_product', id=id))
        try:
            cost_price = float(cost_price)
            margin = float(margin)
            min_stock = int(min_stock)
        except ValueError:
            flash('Valores numéricos inválidos.', 'warning')
            return redirect(url_for('products.edit_product', id=id))
        existing = query_db('SELECT id FROM products WHERE barcode = ? AND id <> ?;', (barcode, id), one=True)
        if existing:
            flash('Outro produto utiliza esse mesmo código de barras.', 'warning')
            return redirect(url_for('products.edit_product', id=id))
        sale_price = calculate_sale_price(cost_price, margin)
        execute_db(
            'UPDATE products SET barcode = ?, name = ?, description = ?, category = ?, brand = ?, cost_price = ?, margin = ?, sale_price = ?, min_stock = ?, unit = ? WHERE id = ?;', 
            (barcode, name, description, category, brand, cost_price, margin, sale_price, min_stock, unit, id)
        )
        flash('Produto atualizado.', 'success')
        return redirect(url_for('products.list_products'))
    return render_template('product_form.html', product=product)
