from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models.db import query_db, execute_db
from models.helpers import get_manager_by_password, calculate_sale_price
import qrcode
import io
import base64
from routes.auth import login_required

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/search-customers')
@login_required
def search_customers():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
    customers = query_db(
        'SELECT id, name, cpf_cnpj FROM customers WHERE status = ? AND (name LIKE ? OR cpf_cnpj LIKE ?) ORDER BY name LIMIT 10;',
        ('Ativo', f'%{q}%', f'%{q}%')
    )
    return jsonify([dict(c) for c in customers])

@sales_bp.route('/search-products')
@login_required
def search_products():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
    products = query_db(
        'SELECT id, barcode, name, sale_price, stock FROM products WHERE stock > 0 AND (barcode LIKE ? OR name LIKE ?) ORDER BY name LIMIT 10;',
        (f'%{q}%', f'%{q}%')
    )
    return jsonify([dict(p) for p in products])

@sales_bp.route('/generate-pix/<float:amount>')
@login_required
def generate_pix(amount):
    # Simulação de chave PIX (email)
    pix_key = 'compras@eletrotech.com.br'
    description = f'Pagamento EletroTech - R$ {amount:.2f}'
    
    # Gerar QR Code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(f'pix:{pix_key}?amount={amount}&description={description}')
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return jsonify({'qr_code': img_base64, 'pix_key': pix_key, 'amount': amount})


def _cart_total(cart):
    return round(sum(item['unit_price'] * item['quantity'] for item in cart), 2)

@sales_bp.route('/', methods=['GET', 'POST'])
@login_required
def pdv():
    payment_methods = query_db('SELECT * FROM payment_methods WHERE active = 1 ORDER BY name;')
    cart = session.get('cart', [])
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            product_id = int(request.form['product_id'])
            quantity = int(request.form['quantity'])
            product = query_db('SELECT * FROM products WHERE id = ?;', (product_id,), one=True)
            if not product:
                flash('Produto inválido.', 'danger')
                return redirect(url_for('sales.pdv'))
            if quantity <= 0:
                flash('Quantidade inválida.', 'warning')
                return redirect(url_for('sales.pdv'))
            existing = next((item for item in cart if item['product_id'] == product_id), None)
            requested = quantity + (existing['quantity'] if existing else 0)
            if requested > product['stock']:
                flash(f'Estoque insuficiente para {product["name"]}.', 'danger')
                return redirect(url_for('sales.pdv'))
            if existing:
                existing['quantity'] += quantity
            else:
                cart.append({
                    'product_id': product['id'],
                    'name': product['name'],
                    'unit_price': product['sale_price'],
                    'quantity': quantity,
                })
            session['cart'] = cart
            flash('Item adicionado ao carrinho.', 'success')
            return redirect(url_for('sales.pdv'))
        if action == 'remove':
            index = int(request.form['index'])
            if 0 <= index < len(cart):
                cart.pop(index)
                session['cart'] = cart
            return redirect(url_for('sales.pdv'))
        if action == 'clear':
            session['cart'] = []
            return redirect(url_for('sales.pdv'))
        if action == 'finalize':
            if not cart:
                flash('O carrinho está vazio.', 'warning')
                return redirect(url_for('sales.pdv'))
            customer_id = request.form.get('customer_id')
            if customer_id:
                try:
                    customer_id = int(customer_id)
                except ValueError:
                    customer_id = None
            else:
                customer_id = None
            discount = float(request.form.get('discount') or 0)
            manager_password = request.form.get('manager_password', '')
            if discount < 0 or discount > 100:
                flash('Desconto inválido.', 'warning')
                return redirect(url_for('sales.pdv'))
            if discount > 5 and session.get('role') != 'gerente' and not get_manager_by_password(manager_password):
                flash('Desconto acima de 5% exige senha de gerente.', 'danger')
                return redirect(url_for('sales.pdv'))
            subtotal = _cart_total(cart)
            total_amount = round(subtotal * (1 - discount / 100.0), 2)
            
            # Processar pagamentos múltiplos
            payments = []
            total_paid = 0.0
            for pm in payment_methods:
                amount_str = request.form.get(f'payment_{pm["id"]}')
                if amount_str:
                    try:
                        amount = float(amount_str)
                        if amount > 0:
                            payments.append({'method_id': pm['id'], 'amount': amount})
                            total_paid += amount
                    except ValueError:
                        pass
            
            if abs(total_paid - total_amount) > 0.01:
                flash('Total pago não corresponde ao valor da venda.', 'danger')
                return redirect(url_for('sales.pdv'))
            
            # Verificar estoque
            for item in cart:
                product = query_db('SELECT * FROM products WHERE id = ?;', (item['product_id'],), one=True)
                if not product or item['quantity'] > product['stock']:
                    flash(f'Estoque insuficiente para {item["name"]}.', 'danger')
                    return redirect(url_for('sales.pdv'))
            
            # Criar venda
            sale_id = execute_db(
                'INSERT INTO sales (customer_id, user_id, datetime, total_amount, discount, payment_method, cash_received, change_amount, coupon, returned) '
                'VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?, 0, 0, ?, 0);',
                (customer_id or None, session['user_id'], total_amount, discount, 'Múltiplas', 'CUPOM-ELETROTECH')
            )
            
            # Inserir pagamentos
            for payment in payments:
                execute_db('INSERT INTO sale_payments (sale_id, payment_method_id, amount) VALUES (?, ?, ?);', 
                          (sale_id, payment['method_id'], payment['amount']))
            
            # Inserir itens e atualizar estoque
            for item in cart:
                execute_db(
                    'INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?);',
                    (sale_id, item['product_id'], item['quantity'], item['unit_price'], item['quantity'] * item['unit_price'])
                )
                execute_db('UPDATE products SET stock = stock - ? WHERE id = ?;', (item['quantity'], item['product_id']))
                execute_db(
                    'INSERT INTO stock_movements (product_id, user_id, datetime, type, quantity, description) VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?);',
                    (item['product_id'], session['user_id'], 'Saída', item['quantity'], f'Venda #{sale_id}')
                )
            session['cart'] = []
            flash('Venda finalizada com sucesso.', 'success')
            return redirect(url_for('sales.receipt', sale_id=sale_id))
    total = _cart_total(cart)
    return render_template('sales_pdv.html', payment_methods=payment_methods, cart=cart, total=total)

@sales_bp.route('/receipt/<int:sale_id>')
@login_required
def receipt(sale_id):
    sale = query_db('SELECT s.*, c.name AS customer_name, u.username AS user_name FROM sales s '
                    'LEFT JOIN customers c ON c.id = s.customer_id LEFT JOIN users u ON u.id = s.user_id WHERE s.id = ?;', (sale_id,), one=True)
    if not sale:
        flash('Venda não encontrada.', 'danger')
        return redirect(url_for('dashboard.index'))
    items = query_db('SELECT si.*, p.name AS product_name FROM sale_items si LEFT JOIN products p ON p.id = si.product_id WHERE si.sale_id = ?;', (sale_id,))
    payments = query_db('SELECT sp.amount, pm.name AS method_name FROM sale_payments sp LEFT JOIN payment_methods pm ON pm.id = sp.payment_method_id WHERE sp.sale_id = ?;', (sale_id,))
    return render_template('sale_receipt.html', sale=sale, items=items, payments=payments)

@sales_bp.route('/list')
@login_required
def sale_list():
    sales = query_db(
        'SELECT s.*, c.name AS customer_name, u.username AS user_name FROM sales s '
        'LEFT JOIN customers c ON c.id = s.customer_id LEFT JOIN users u ON u.id = s.user_id ORDER BY s.datetime DESC LIMIT 100;'
    )
    return render_template('sale_list.html', sales=sales)

@sales_bp.route('/return/<int:sale_id>', methods=['POST'])
@login_required
def sale_return(sale_id):
    sale = query_db('SELECT * FROM sales WHERE id = ?;', (sale_id,), one=True)
    if not sale:
        flash('Venda não encontrada.', 'danger')
        return redirect(url_for('sales.sale_list'))
    if sale['returned']:
        flash('Venda já estornada.', 'warning')
        return redirect(url_for('sales.sale_list'))
    items = query_db('SELECT * FROM sale_items WHERE sale_id = ?;', (sale_id,))
    for item in items:
        execute_db('UPDATE products SET stock = stock + ? WHERE id = ?;', (item['quantity'], item['product_id']))
        execute_db(
            'INSERT INTO stock_movements (product_id, user_id, datetime, type, quantity, description) VALUES (?, ?, CURRENT_TIMESTAMP, ?, ?, ?);',
            (item['product_id'], session['user_id'], 'Entrada', item['quantity'], f'Estorno Venda #{sale_id}')
        )
    execute_db('UPDATE sales SET returned = 1 WHERE id = ?;', (sale_id,))
    flash('Estorno realizado e estoque reabastecido.', 'success')
    return redirect(url_for('sales.sale_list'))
