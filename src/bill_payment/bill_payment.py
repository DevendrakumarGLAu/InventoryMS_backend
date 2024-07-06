from src.DB_connect.dbconnection import Dbconnect
from src.dataframe_df.dataframe_operations import Dataframe_pandas


class Bill_payments:
    @staticmethod
    def save_orders(table_name, column_data):
        try:
            connection = Dbconnect.dbconnects()
            if connection:
                cursor = connection.cursor()
                total_bill_price = 0
                # Iterate over each order in column_data['orders']
                for order in column_data['orders']:
                    category_id = order['category_id']
                    product_id = order['product_id']
                    quantity = int(order['quantity'])
                    selling_price = float(order['selling_price'])

                    total_selling_price = quantity * selling_price
                    total_bill_price += total_selling_price
                    update_query = f"""
                        UPDATE add_product_details 
                        SET quantity = quantity - {quantity},
                            selling_price = {selling_price},
                            total_selling_price = {total_selling_price},
                            total_bill_price = {total_bill_price}
                        WHERE category = '{category_id}' AND productname = '{product_id}'
                    """
                    cursor.execute(update_query)
                    print(f"Executed query: {update_query}")
                    connection.commit()
                return {'status': 'success', 'message': 'Orders saved successfully'}
            else:
                return {'status': 'error', 'message': 'Failed to connect to the database'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    # @staticmethod
    # def get_order_details(order_id):
    #     db_connection = Dbconnect()
    #     connection = db_connection.dbconnects()
    #     if connection:
    #         cursor = connection.cursor(dictionary=True)  # Set dictionary cursor to get results as dictionaries
    #         try:
    #             # Query to retrieve order details for a specific order ID
    #             cursor.execute("""
    #                     SELECT *
    #                     FROM OrderDetails
    #                     WHERE order_id = %s
    #                 """, (order_id,))
    #             order_details = cursor.fetchall()
    #             return {"order_details": order_details, "status": "success"}
    #         except Exception as e:
    #             return {"error": str(e), "status": "error"}
    #         finally:
    #             cursor.close()
    #             connection.close()
    #     else:
    #         return {"error": "Failed to connect to the database", "status": "error"}