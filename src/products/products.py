import json

from flask import jsonify


import pandas as pd

from src.DB_connect.dbconnection import Dbconnect
from src.dataframe_df.dataframe_operations import Dataframe_pandas
from datetime import datetime


class Product:
    def __init__(self):
        self.db_connection = Dbconnect()

    @staticmethod
    def update_product(id, category,category_id,product_id, quantity, productName, costPrice, manufacturingDate, expiryDate):
        connection = Product().db_connection.dbconnects()

        if connection:
            try:
                cursor = connection.cursor()
                manufacturing_date_obj = datetime.strptime(manufacturingDate, '%Y-%m-%d')
                expiry_date_obj = datetime.strptime(expiryDate, '%Y-%m-%d')
                manufacturing_date_str = manufacturing_date_obj.strftime('%Y-%m-%d')
                expiry_date_str = expiry_date_obj.strftime('%Y-%m-%d')
                # Update query with id placeholder
                remaining_stock = quantity
                CostPerPiece =float(costPrice / quantity)
                sql_query = f"UPDATE products SET category=%s,category_id=%s,product_id=%s, quantity=%s, productName=%s, costPrice=%s, manufacturingDate=%s, expiryDate=%s, remaining_stock=%s,CostPerPiece=%s WHERE id=%s"
                cursor.execute(sql_query, (
                    category,category_id,product_id, quantity, productName, costPrice, manufacturing_date_str, expiry_date_str,remaining_stock,CostPerPiece, id))
                connection.commit()
                cursor.close()
                connection.close()

                return {"message": "Data updated successfully",
                        "status":"success"},200
            except Exception as e:
                return {"message":"Error in update data",
                    "error": str(e)}
        else:
            return {"message": "Failed to connect to MySQL database"}

    @staticmethod
    def save_product(category,category_id,product_id, quantity, productName, costPrice,  manufacturingDate, expiryDate):
        connection = Product().db_connection.dbconnects()
        if connection:
            try:
                cursor = connection.cursor()

                check_duplicate_prdct_name= f"SELECT * FROM products WHERE productName = '{productName}'"
                cursor.execute(check_duplicate_prdct_name)
                existing_product = cursor.fetchone()
                remaining_stock=0
                if existing_product:

                    return {"message": "Please edit Quantity in stock, Product already exists.", "status": "error"}
                remaining_stock += int(quantity)
                costPrice1 = float(costPrice)
                quantity1 = float(quantity)
                CostPerPiece =costPrice1/quantity1
                print(CostPerPiece)
                # Insert query
                sql_query = "INSERT INTO products (category,category_id,product_id, quantity, productName, costPrice,  manufacturingDate, expiryDate,remaining_stock,CostPerPiece) VALUES (%s, %s, %s, %s, %s, %s,%s,%s,%s, %s)"
                cursor.execute(sql_query, (
                    category,category_id,product_id, quantity, productName, costPrice,  manufacturingDate, expiryDate,remaining_stock,CostPerPiece))
                connection.commit()
                cursor.close()
                connection.close()

                return {"message": "Data saved successfully",
                        "status":"success"}
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"message": "Failed to connect to MySQL database"}

    @staticmethod
    def get_products():
        try:
            query = "SELECT * FROM products"
            products_df = Dataframe_pandas.read_sql_as_df(query)
            if products_df is not None:
                # Convert datetime columns to ISO format
                products_df['manufacturingDate'] = products_df['manufacturingDate'].astype(str)
                products_df['expiryDate'] = products_df['expiryDate'].astype(str)

                products_json = json.loads(products_df.to_json(orient='records'))
                return jsonify({'data': products_json,
                                'message':'Data delivered successfull',
                                'status':'success'})
            else:
                return jsonify({'error': 'Failed to fetch products data'})
        except Exception as e:
            return jsonify({'error': str(e)})

    def get_product_by_id(self,id):
        try:
            sql_query = f"""SELECT * FROM products WHERE id = {id}"""
            # Pass the id parameter to the read_sql_as_df function
            products_df = Dataframe_pandas.read_sql_as_df(sql_query)
            if products_df is not None:
                products_json = json.loads(products_df.to_json(orient='records'))
                return jsonify({'data': products_json,
                                'message':"Data fetch succesfully",
                                'status':'success'
                                })
            else:
                return jsonify({'message': 'Failed to fetch products data',
                                "status":"error"})
        except Exception as e:
            return {"status": str(e),
                    "message":"failed to fetch Data"}

    @staticmethod
    def get_category_id(Table_name):
        query = f"SELECT * FROM {Table_name}"
        try:
            df=  Dataframe_pandas.read_sql_as_df(query)
            if df is not None and not df.empty:
                categories = df.to_dict('records')
                return {
                    "data":categories,
                    "message":"Data Fetched successfully",
                    "status":"success"
                }
            else:
                return {
                    "data":[],
                    "message":"No Data Found",
                    "status":"error"
                }
        except Exception as e:
            return {"error":f"Error: {e}",
                    "message":"Error while fetch category",
                    "status":"error"}

    @staticmethod
    def get_products_name(category_id):
        query = f""" SELECT productname.id AS product_id, productname.name AS product_name
                    FROM productname JOIN category ON productname.category_id = category.id WHERE category.id = {category_id}; """
        try:
            products_df = Dataframe_pandas.read_sql_as_df(query)
            if products_df is not None:
                products_df = products_df.to_dict('records')
                return {
                    "data": products_df,
                    "message": "Data Fetched successfully",
                    "status": "success"
                }
            else:
                return {
                    "data": [],
                    "message": "No Data Found",
                    "status": "error"
                }
        except Exception as e:
            return {"error":f"Error: {e}",
                    "message":"Error while fetch category",
                    "status":"error"}
