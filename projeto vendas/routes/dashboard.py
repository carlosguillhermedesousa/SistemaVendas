from flask import Blueprint, render_template
from models.db import query_db
from routes.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    total_vendas = query_db('SELECT COUNT(*) AS count FROM sales WHERE returned = 0;', (), one=True)['count']
    receita = query_db('SELECT IFNULL(SUM(total_amount), 0) AS total FROM sales WHERE returned = 0;', (), one=True)['total']
    produtos_baixo = query_db('SELECT COUNT(*) AS count FROM products WHERE stock <= min_stock; ', (), one=True)['count']
    vendas_recentes = query_db(
        'SELECT s.id, s.datetime, c.name AS customer_name, s.total_amount FROM sales s LEFT JOIN customers c ON c.id = s.customer_id ORDER BY s.datetime DESC LIMIT 5;'
    )
    movimentos_recentes = query_db(
        'SELECT m.datetime, p.name AS product_name, m.type, m.quantity, u.username AS user_name FROM stock_movements m '
        'LEFT JOIN products p ON p.id = m.product_id LEFT JOIN users u ON u.id = m.user_id '
        'ORDER BY m.datetime DESC LIMIT 5;'
    )
    return render_template(
        'dashboard.html',
        total_vendas=total_vendas,
        receita=receita,
        produtos_baixo=produtos_baixo,
        vendas_recentes=vendas_recentes,
        movimentos_recentes=movimentos_recentes,
    )
