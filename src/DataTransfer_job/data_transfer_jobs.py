from pickle import STRING

import mysql
import pandas as pd
from flask import jsonify

from src.DB_connect.dbconnection import Dbconnect
import json

from src.dataframe_df.dataframe_operations import Dataframe_pandas
from src.validation.validations import Validators


class DataTransfer:
    @staticmethod
    def create_data_operation(id,table_name,sql_insert):
        message = ''
        db_connection = Dbconnect()
        connection = db_connection.dbconnects()
        if connection:
            cursor = connection.cursor()
            try:
                create_objects_sql = f"CREATE TABLE {table_name} ({sql_insert})"
                cursor.execute(create_objects_sql)
                message = 'Table created successfully'
            except mysql.connector.Error as error:
                message = f'Error creating table: {error}'
            finally:
                cursor.close()
                connection.close()
            return message
        else:
            return 'Failed to connect to the database'


    @staticmethod
    def save_data_operation(table_name, column_data, action):
        try:
            db_connection = Dbconnect()
            connection = db_connection.dbconnects()
            validation_flag = 0
            if table_name == 'vendors' or table_name == 'users_details':
                validation_result = Validators.validate_vendor_data(column_data, connection, table_name)
                if validation_result['status'] == 'error':
                    return validation_result
            # if table_name == 'users_details':
            #     validation_result = Validators.Validator_userDetails(column_data, connection,table_name)
            #     if validation_result['status'] == 'error':
            #         return validation_result
            if table_name == 'category' or table_name == 'productname':
                new_name = column_data['name']
                duplicate_check_result = DataTransfer.check_duplicate(table_name,new_name)
                if duplicate_check_result['status'] == 'error':
                    return duplicate_check_result

            if connection:
                column_data_json =column_data
                data_set = pd.json_normalize(column_data_json)
                Dataframe_pandas.write_df_to_sql(data_set, table_name, operation='REPLACE')
            if validation_flag == 1:
                message = 'Fields has ann Empty Value',
                status = "error"
            else:
                message = 'Data transferred successfully'
                status = 'success'
            return {
                "message":message,
                "status":status
            }

        except Exception as e:
            raise e

    @staticmethod
    def delete_data_operation(table_name, row_id):
        db_connection = Dbconnect()
        connection = db_connection.dbconnects()
        if connection:
            try:
                cursor = connection.cursor()
                if not isinstance(row_id, int):
                    return {'status': 'Error', 'message': 'Row ID must be an integer'}

                delete_sql = f"DELETE FROM {table_name} WHERE id = {row_id}"
                cursor.execute(delete_sql)  # Corrected method name
                connection.commit()
                if cursor.rowcount == 0:
                    return {'status': 'Error', 'message': 'No data found to delete'}
                else:
                    return {'status': 'success', 'message': 'Data deleted successfully'}
                # return {'status': 'success', 'message': message}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
        else:
            return {'status': 'error', 'message': 'Failed to connect to the database'}

    @staticmethod
    def sell_product(id, sell_quantity, unit_sellingPrice):
        db_connection = Dbconnect()
        connection = db_connection.dbconnects()
        cursor = connection.cursor()
        try:
            get_query = f"select * from products where id = {id}"
            result = Dataframe_pandas.read_sql_as_df(get_query)
            if result.empty:
                return {'status': 'error', 'message': 'Product not found'}

            result_dict = result.to_dict(orient='records')
            product_data = result_dict[0]

            if product_data['Total_sales'] is None:
                product_data['Total_sales'] = 0
            if product_data['total_quantity_sold'] is None:
                product_data['total_quantity_sold'] = 0
            if product_data['remaining_stock'] == 0:
                product_data['remaining_stock'] =product_data['quantity']
            if product_data['remaining_stock'] is None :
                product_data['remaining_stock'] = 0
            if product_data['unit_sellingPrice'] is None:
                product_data['unit_sellingPrice'] = 0
            if product_data['sell_quantity'] is None:
                product_data['sell_quantity'] = 0

            # print("reamaing stock",product_data['remaining_stock'])
            # print("quantity",product_data['quantity'])
            # Calculate remaining_stock after the sale

            remaining_stock = product_data['remaining_stock'] - sell_quantity
            if remaining_stock < 0:
                return {
                    "status": "error",
                    "message": f"Not enough stock available. Available quantity: {product_data['remaining_stock']}"
                }
            if product_data['total_quantity_sold'] == product_data['quantity']:
                return {
                    "status": "error",
                    "message": "Stock depleted. Please restock the inventory."
                }
            elif product_data['total_quantity_sold'] < product_data['quantity'] and product_data[
                'remaining_stock'] == 0:
                return {
                    "status": "error",
                    "message": "Stock quantity mismatch. Please update the inventory records."
                }

            product_data['unit_sellingPrice'] = unit_sellingPrice
            net_sellingPrice = sell_quantity * unit_sellingPrice
            product_data['sell_quantity'] = sell_quantity
            product_data['net_sellingPrice'] = net_sellingPrice
            product_data['Total_sales'] += net_sellingPrice
            product_data['total_quantity_sold'] += sell_quantity


            update_query = f"""
                UPDATE products 
                SET sell_quantity = {product_data['sell_quantity']},
                    unit_sellingPrice = {product_data['unit_sellingPrice']}, 
                    remaining_stock = {remaining_stock},
                    net_sellingPrice = {product_data['net_sellingPrice']},
                    Total_sales = {product_data['Total_sales']},
                    total_quantity_sold = {product_data['total_quantity_sold']}
                WHERE id = {id}
            """
            # Execute the SQL update query
            cursor.execute(update_query)
            connection.commit()
            return {'status': 'success', 'message': 'Product updated successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    @staticmethod
    def check_duplicate(table, new_name):
        db_connection = Dbconnect()
        connection = db_connection.dbconnects()
        cursor = connection.cursor()

        if connection:
            try:
                query = f"SELECT name FROM {table}"
                cursor.execute(query)
                rows = cursor.fetchall()
                existing_names = {row[0] for row in rows}
                if new_name in existing_names:
                    return {'status': 'error', 'message': f'{new_name} already exists'}
                return {'status': 'success'}
            except Exception as e:
                return {'status': 'error', 'message': str(e)}
            finally:
                cursor.close()
                connection.close()
        else:
            return {'status': 'error', 'message': 'Failed to connect to the database'}

    @staticmethod
    def update_data_operation(row_id, column_data, table_name):
        try:
            db_connection = Dbconnect()
            connection = db_connection.dbconnects()
            if connection:
                # Convert column_data to a DataFrame
                data_df = pd.DataFrame([column_data])

                # Construct the SET clause for the SQL update query
                set_clause = ', '.join([f"{key} = '{value}'" for key, value in column_data.items()])

                # Construct the SQL update query
                update_query = f"UPDATE {table_name} SET {set_clause} WHERE id = {row_id}"

                # Execute the update query
                cursor = connection.cursor()
                cursor.execute(update_query)
                connection.commit()

                # Check if any rows were affected
                if cursor.rowcount > 0:
                    return {'status': 'success', 'message': 'Data updated successfully'}
                else:
                    return {'status': 'error', 'message': 'No rows were updated'}
            else:
                return {'status': 'error', 'message': 'Failed to connect to the database'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
