from app import create_app
from flask import render_template

app = create_app()
with app.test_request_context('/sales'):
    print(render_template('sales_pdv.html', payment_methods=[{'id':1,'name':'Dinheiro'}], cart=[], total=0))
