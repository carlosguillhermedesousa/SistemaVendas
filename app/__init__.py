import os
from flask import Flask, redirect, request, session, url_for
from models.db import init_db


def create_app():
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    template_dir = os.path.join(root_path, 'templates')
    static_dir = os.path.join(root_path, 'static')
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'eletrotech-distribuidora-2026'),
        DATABASE=os.path.join(root_path, 'database', 'eletrotech.db'),
    )

    os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'database'), exist_ok=True)

    init_db(app)

    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.customers import customers_bp
    from routes.products import products_bp
    from routes.stock import stock_bp
    from routes.sales import sales_bp
    from routes.payment_methods import payment_methods_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(customers_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(stock_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(payment_methods_bp)

    @app.before_request
    def require_login():
        if request.endpoint is None:
            return None
        if request.endpoint == 'static':
            return None
        if request.endpoint.startswith('auth.'):
            return None
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return None

    @app.after_request
    def add_no_cache_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    return app
