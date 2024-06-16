from src.DB_connect.dbconnection import Dbconnect


class Validators:
    @staticmethod
    def validate_vendor_data(column_data, connection,table_name):
        if 'email' in column_data:
            email = column_data['email']
            cursor = connection.cursor()
            cursor.execute(f"SELECT id FROM {table_name} WHERE email = '{email}'")
            if cursor.fetchone():
                return {'status': 'error', 'message': f'Email "{email}" already exists'}

        if 'mobile' in column_data:
            result = column_data['mobile']
            # Check if the mobile number already exists in the table
            cursor.execute(f"SELECT id FROM vendors WHERE mobile = '{result}'")
            if cursor.fetchone():
                return {'status': 'error', 'message': f'Mobile number "{result}" already exists'}
        if 'phone' in column_data: #for users_details table phone in column
            result = column_data['phone']
            cursor.execute(f"SELECT id FROM {table_name} WHERE phone = '{result}'")
            if cursor.fetchone():
                return {'status': 'error', 'message': f'Mobile number "{result}" already exists'}
        return {'status': 'success'}

    @staticmethod
    def Validator_userDetails(column_data, connection):
        if 'email' in column_data:
            email = column_data['email']
            cursor = connection.cursor()
            cursor.execute(f"SELECT id FROM vendors WHERE email = '{email}'")
            if cursor.fetchone():
                return {'status': 'error', 'message': f'Email "{email}" already exists'}

