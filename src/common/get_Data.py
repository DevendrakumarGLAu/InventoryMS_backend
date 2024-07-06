import json
import math
import traceback

import pandas as pd
from flask import jsonify

from src.DB_connect.dbconnection import Dbconnect
from src.dataframe_df.dataframe_operations import Dataframe_pandas


class GetData:
    @staticmethod
    def getData_common(id, Table_name):
        try:
            if id:
                sql_query = f"""SELECT * FROM {Table_name} WHERE id = {id}"""
            else:
                if Table_name == 'add_product_details':
                    sql_query = f"""SELECT apd.id, apd.quantity, apd.price, apd.manufacturingDate, apd.expiryDate, c.name AS category, p.name AS productName
                                FROM add_product_details apd
                                LEFT JOIN category c ON apd.category = c.id
                                LEFT JOIN productname p ON apd.productName = p.id
                                ORDER BY apd.id desc;"""
                else:
                    sql_query = f"""SELECT * FROM {Table_name} ORDER BY id DESC"""
            print(sql_query)
            # Pass the id parameter to the read_sql_as_df function
            df = Dataframe_pandas.read_sql_as_df(sql_query)
            if df is not None:
                products_json = json.loads(df.to_json(orient='records'))
                return jsonify({'data': products_json,
                                'message': "Data fetch succesfully",
                                'status': 'success'
                                })
            else:
                return jsonify({'message': 'Failed to fetch products data',
                                "status": "error"})
        except Exception as e:
            return {"status": str(e),
                    "message": "failed to fetch Data"}

    @staticmethod
    def get_saved_order():
        connection = Dbconnect.dbconnects()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute("""
                    SELECT 
                        o.name, o.mobile,
                        oi.sno, oi.category_id, oi.product_id, oi.quantity, oi.category_name, oi.product_name
                    FROM 
                        Orders o
                    JOIN 
                        OrderDetails oi ON o.order_id = oi.order_id
                """)
                saved_orders = cursor.fetchall()

                # Initialize variables to store name, mobile, and orders
                name = None
                mobile = None
                orders = []

                # Iterate over the saved_orders to extract name, mobile, and orders
                for order in saved_orders:
                    name = order['name']
                    mobile = order['mobile']
                    orders.append({
                        "sno": order['sno'],
                        "category_id": order['category_id'],
                        "product_id": order['product_id'],
                        "quantity": order['quantity'],
                        "category_name": order['category_name'],
                        "product_name": order['product_name']
                    })

                # Construct the response dictionary
                response = {
                    "name": name,
                    "mobile": mobile,
                    "orders": orders,
                                    }

                return {"data":response,
                        "message":"Data fetch successfully",
                        "status":"success"}
            except Exception as e:
                return {"error": str(e), "status": "error"}
            finally:
                cursor.close()
                connection.close()
        else:
            return {"error": "Failed to connect to the database", "status": "error"}

    @staticmethod
    def sidebar_menu_config(AccountId):

        connection = Dbconnect.dbconnects()
        if connection:
            try:
                cursor = connection.cursor()
                query = f"""SELECT 
                            m.id,                        
                                rp.`view`, 
                                rp.edit, 
                                rp.`delete`, 
                                rp.`add`,
                                m.parent_id,
                                m.label, m.route, m.icon, m.display_order
                            FROM 
                                roles_permissions rp
                            LEFT JOIN 
                                users_details ud ON ud.`role` = rp.role_id
                            left join menuitems m on rp.menuId = m.id
                            where m.parent_id is null and ud.id = {AccountId} order by display_order;"""
                result = Dataframe_pandas.read_sql_as_df(query)
                json_data = result.to_json(orient="records")
                result = json.loads(json_data)
                child = []
                if not result:
                    response = {
                        "message": "Data not found", "status": "error"
                    }
                    return jsonify(response)
                for item in result:
                    item['childmenu'] = GetData.user_childMenu(item['id'], AccountId)
                    if not item['childmenu']:
                        item['childmenu'] = child
                return result
            except Exception as e:
                response = {
                    "message": e,
                    "status": "error",
                    "data": traceback.format_exc()
                }
                return jsonify(response)

    @staticmethod
    def user_childMenu(id, AccountId):
        query = f"""SELECT m.id,
                            rp.`view`, 
                            rp.edit, 
                            rp.`delete`, 
                            rp.`add`,
                            m.parent_id,
                            m.label, m.route, m.icon, m.display_order
                        FROM 
                            roles_permissions rp
                        LEFT JOIN 
                            users_details ud ON ud.`role` = rp.role_id
                        left join menuitems m on rp.menuId = m.id
                        where m.parent_id = {id} and ud.id = {AccountId} order by display_order;"""
        result = Dataframe_pandas.read_sql_as_df(query)
        json_data = result.to_json(orient="records")
        result = json.loads(json_data)
        child = []
        for item in result:
            item['childmenu'] = GetData.user_childMenu(item['id'], AccountId)
            if not item['childmenu']:
                item['childmenu'] = child
        return result



