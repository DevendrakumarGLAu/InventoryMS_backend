import json
import math

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
                sql_query = f"""SELECT * FROM {Table_name} ORDER BY id DESC"""
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
    def sidebar_menu_config():
        connection = Dbconnect.dbconnects()
        if connection:
            try:
                cursor = connection.cursor()
                query = f"""SELECT * FROM menuitems"""
                cursor.execute(query)
                result = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                df = pd.DataFrame(result, columns=columns)
                sidebar_menu_config = []
                for index, row in df.iterrows():
                    menu_item = {
                        'label': row['label'],
                        'route': row['route'],
                        'icon': row['icon']
                    }
                    parent_id = row['parent_id']
                    if not isinstance(parent_id, float) or not math.isnan(parent_id):
                        parent_id_int = int(parent_id)  # Convert float to integer
                        submenu_query = f"SELECT * FROM menuitems WHERE parent_id = {parent_id_int}"
                        cursor.execute(submenu_query)
                        submenu_result = cursor.fetchall()
                        submenu = []
                        for sub_row in submenu_result:
                            submenu_item = {
                                'label': sub_row[1],  # Assuming 'label' is the second column
                    'route': sub_row[2],  # Assuming 'route' is the third column
                    'icon': sub_row[3],
                            }
                            submenu.append(submenu_item)
                        if parent_id_int == 2:
                            menu_item['submenu'] = submenu
                    sidebar_menu_config.append(menu_item)
                    print(sidebar_menu_config)
                return jsonify(sidebar_menu_config)
            except Exception as e:
                print('Error retrieving sidebar menu configuration:', e)
                return {
                    "message":e
                }