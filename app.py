import requests
from flask import Flask, request, jsonify  # Import request object
from flask_cors import CORS

# from src.routes.routes import Routes

from src.DB_connect.dbconnection import Dbconnect
from src.app_decorator.app_decorator import app_decorator
from src.common.get_Data import GetData
from src.config import SECRET_KEY
from src.routes.routes import Routes

METHODS = ['GET', 'POST']

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = SECRET_KEY['secret_key']

@app.route('/mysql', methods=METHODS)
def connectionss():
    db_connection = Dbconnect()
    connection = db_connection.dbconnects()
    if connection:
        return 'Connected to MySQL database'
    else:
        return 'Failed to connect to MySQL database'

@app.route('/addproduct', methods=METHODS)
@app_decorator
def add_product():
    return Routes.addproduct(request)

@app.route('/getproducts', methods=METHODS)
@app_decorator
def get_products():
    return Routes.get_products()

@app.route('/get_productby_id', methods=METHODS)
@app_decorator
def get_product():
    return Routes.get_product(request)

@app.route('/getdata_for_all', methods= METHODS)
@app_decorator
def get_category():
    return Routes.get_category_name(request)

@app.route('/db_operation', methods=METHODS)
@app_decorator
def db_operations():
    return Routes.db_operations(request)

@app.route('/get_products_by_category',methods=METHODS)
@app_decorator
def get_products_by_category():
    return Routes.get_products_by_category(request)

@app.route('/product_sales',methods=METHODS)
@app_decorator
def product_sells():
    return Routes.sell_product(request)

@app.route('/login',methods=METHODS)
def login_api():
    return Routes.login_api(request)

@app.route('/save_order',methods= METHODS)
@app_decorator
def save_order():
    return Routes.save_order(request)

@app.route('/get_saved_order', methods= METHODS)
@app_decorator
def get_saved_order():
    return Routes.get_saved_order()


@app.route('/getData_common', methods = METHODS)
@app_decorator
def getData_common():
    return Routes.getData_common(request)

@app.route('/sidebarMenuConfig', methods = METHODS)
def sidebar_menu_config():
    return GetData.sidebar_menu_config()

if __name__ == '__main__':
    app.run(debug=True)
