from flask import jsonify

from src.DB_connect.dbconnection import Dbconnect
# from src.JWTTokens.generate_token import JwtTokens
from src.JWTTokens.generate_token import generate_token
from src.dataframe_df.dataframe_operations import Dataframe_pandas


class Login:

    @staticmethod
    def login_api(email,password):
        from src.DB_connect.dbconnection import Dbconnect
        db_connection = Dbconnect()
        connection =db_connection.dbconnects()
        if connection:
            try:
                cursor = connection.cursor()
                # query = f"""SELECT * FROM users_details WHERE email = '{email}' AND password = '{password}'"""
                query = f"""SELECT u.id, u.name, u.email, u.phone, u.address, u.role, u.action, u.confirmPassword, r.role_name,r.id as role_id
FROM users_details u
JOIN roles r ON u.role = r.id
WHERE u.email = '{email}' AND u.password = '{password}';
"""
                # cursor.execute(query)
                # result = cursor.fetchone()
                result = Dataframe_pandas.read_sql_as_df(query)
                if not result.empty:
                    role_id = result.at[0, 'role_id']
                    token = generate_token(email,role_id)
                    result_dict = result.to_dict(orient='records')
                    response_data = {
                        "data": result_dict,
                        "token": token,
                        "message": "login successful",
                        "status": "success"
                    }
                    return jsonify(response_data)

                else:
                    return {"data":[],
                        "message":"invalid credentials",
                            "status":"error"}
            except Exception as e:
                return {"error": str(e)}
            finally:
                cursor.close()
                connection.close()
        else:
            return {"error": "Failed to connect to the database"}