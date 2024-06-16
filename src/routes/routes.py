from flask import jsonify

from src.DataTransfer_job.data_transfer_jobs import DataTransfer
from src.bill_payment.bill_payment import Bill_payments
from src.common.get_Data import GetData
from src.fetchParameter.fetchparameter import Fetchparameters
from src.login.login import Login
from src.products.products import Product

class Routes:
    @staticmethod
    def addproduct(request):
        id = Fetchparameters.fetch_parameter(request, 'id', type=int)
        category = Fetchparameters.fetch_parameter(request, 'category', type=str)
        category_id = Fetchparameters.fetch_parameter(request, 'category_id', type=int)
        product_id = Fetchparameters.fetch_parameter(request, 'product_id', type=int)
        quantity = Fetchparameters.fetch_parameter(request, 'quantity', type=int)
        productName = Fetchparameters.fetch_parameter(request, 'productName', type=str)
        costPrice = Fetchparameters.fetch_parameter(request, 'costPrice', type=int)
        manufacturingDate = Fetchparameters.fetch_parameter(request, 'manufacturingDate', type=str)
        expiryDate = Fetchparameters.fetch_parameter(request, 'expiryDate', type=str)

        if id is not None:
            print(id)
            result = Product.update_product(id, category,category_id,product_id, quantity, productName, costPrice, manufacturingDate,expiryDate)
        else:
            result = Product.save_product(category,category_id,product_id, quantity, productName, costPrice, manufacturingDate, expiryDate)
        return result

    @staticmethod
    def get_product(request):
        id = Fetchparameters.fetch_parameter(request, 'id', type=int)
        result = Product().get_product_by_id(id)
        return result


    @staticmethod
    def get_products():
        return Product.get_products()

    @staticmethod
    def db_operations(request):
        id = Fetchparameters.fetch_parameter(request, 'id', type=int)
        table_name = Fetchparameters.fetch_parameter(request, 'table_name', type=str)
        action_mode = Fetchparameters.fetch_parameter(request,'action')

        if action_mode =="create":
            sql_insert = Fetchparameters.fetch_parameter(request, 'sql_insert')
            result = DataTransfer.create_data_operation(id,table_name,sql_insert)
        elif action_mode == "delete":
            row_ids = Fetchparameters.fetch_parameter(request, 'row_ids', )
            result = DataTransfer.delete_data_operation(table_name, row_ids)
        elif action_mode == "update":
            row_ids = Fetchparameters.fetch_parameter(request, 'id' )
            column_data = Fetchparameters.fetch_parameter(request, 'column_data')
            result = DataTransfer.update_data_operation(row_ids,column_data,table_name)
        else:
            column_data = Fetchparameters.fetch_parameter(request, 'column_data')
            result = DataTransfer.save_data_operation(table_name, column_data, action_mode)
        return result


    @staticmethod
    def login_api(request):
        email = Fetchparameters.fetch_parameter(request, 'email', type=str)
        password= Fetchparameters.fetch_parameter(request,'password',type= str)
        return Login.login_api(email,password)

    @staticmethod
    def sell_product(request):
        id = Fetchparameters.fetch_parameter(request, 'product_id', type=int)
        sell_quantity=Fetchparameters.fetch_parameter(request, 'sell_quantity', type=int)
        unit_sellingPrice = Fetchparameters.fetch_parameter(request, 'unit_sellingPrice', type=int)
        return DataTransfer.sell_product(id,sell_quantity,unit_sellingPrice)


    @staticmethod
    def get_category_name(request):
        Table_name = Fetchparameters.fetch_parameter(request, 'Table_name', type=str)
        return Product.get_category_id(Table_name)

    @staticmethod
    def get_products_by_category(request):
        category_id = Fetchparameters.fetch_parameter(request, 'category_id', type=str)
        return Product.get_products_name(category_id)

    @staticmethod
    def save_order(request):
        name = Fetchparameters.fetch_parameter(request,'name', type = str)
        mobile = Fetchparameters.fetch_parameter(request, 'mobile', type=str)
        data = request.get_json()
        orders = data["orders"]
        result = Bill_payments.save_orders(name,mobile,orders)
        return result

    @staticmethod
    def get_saved_order():
        result = GetData.get_saved_order()
        return result

    @staticmethod
    def getData_common(request):
        id = Fetchparameters.fetch_parameter(request,'id', type = int)
        Table_name = Fetchparameters.fetch_parameter(request, 'Table_name', type=str)
        result = GetData.getData_common(id,Table_name)
        return result


