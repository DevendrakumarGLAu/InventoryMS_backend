import mysql.connector

class Dbconnect:
    @staticmethod
    def dbconnects():
        connection = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password="Dev@1997",
            database ="pharmanage"
        )

        return connection