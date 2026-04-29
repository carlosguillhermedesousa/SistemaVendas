import os
from flask import Flask
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

    return app
