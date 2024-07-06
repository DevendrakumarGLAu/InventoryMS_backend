import logging

import mysql.connector
import os
from dotenv import load_dotenv

class Dbconnect:
    @staticmethod
    def dbconnects():
        load_dotenv()
        host = os.getenv("host")
        port = os.getenv("port")
        user = os.getenv("user")
        password = os.getenv("password")
        database = os.getenv("database")

        try:
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database
            )
            if connection.is_connected():
                db_info = connection.get_server_info()
                print(f"Connected to MySQL Server version {db_info}")
                return connection
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            logging.debug(f"""mysql error {err}""")
            raise err

