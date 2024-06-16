# app_decorator.py

import jwt
from flask import request, jsonify
from functools import wraps

from src.DB_connect.dbconnection import Dbconnect
from src.config import SECRET_KEY

def fetch_roles_permissions(role_id):
    try:
        db_connection = Dbconnect()
        connection = db_connection.dbconnects()
        if connection:
            cursor = connection.cursor(dictionary=True)
            sql_query = f"""
                SELECT `view`, `edit`, `delete`, `add`
                FROM roles_permissions
                WHERE role_id = {role_id}
            """
            cursor.execute(sql_query)
            permissions = cursor.fetchone()
            cursor.close()
            connection.close()
            return permissions
        else:
            return None
    except Exception as e:
        print(f"Error fetching roles permissions: {str(e)}")
        return None

def app_decorator(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # token = None
        token = request.headers.get('Authorization', '').split()[-1]
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            token = auth_header.split(" ")[1] if len(auth_header.split(" ")) > 1 else None

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401


        try:
            payload = jwt.decode(token, SECRET_KEY['secret_key'], algorithms=["HS256"])
            # data = jwt.decode(token, SECRET_KEY['secret_key'], algorithms=["HS256"])
            current_role_id = payload.get('role_id')
            if not current_role_id:
                return jsonify({'message': 'Invalid token!'}), 401
            permissions = fetch_roles_permissions(current_role_id)
            if not permissions:
                return jsonify({'message': 'Unauthorized access!'}), 403
            # if required_permission not in permissions or not permissions[required_permission]:
            #     return jsonify({'message': 'Insufficient permissions!'}), 403

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        permissions = fetch_roles_permissions(current_role_id)

        return f(*args, **kwargs)

    return decorated
