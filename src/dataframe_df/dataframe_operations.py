import pandas as pd

from src.DB_connect.dbconnection import Dbconnect

class Dataframe_pandas:
    @staticmethod
    def read_sql_as_df(query):
        try:
            connection = Dbconnect.dbconnects()
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            columns = [col[0] for col in cursor.description]
            df = pd.DataFrame(result, columns=columns)
            cursor.close()
            connection.close()
            return df

        except Exception as e:
            print(f"Error: {e}")
            return None

    @staticmethod
    def write_df_to_sql(dataframe, table, operation='REPLACE', column_str=None):
        db_connection = Dbconnect()
        connection = db_connection.dbconnects()

        if connection:
            cursor = connection.cursor()
            try:
                tpls = [tuple(x) for x in dataframe.to_numpy()]
                if not column_str:
                    cols = ','.join(list(dataframe.columns))
                else:
                    cols = str(column_str)

                vals = ','.join(['%s'] * len(dataframe.columns))
                sql = f" {operation} INTO %s(%s) VALUES(%s)" % (table, cols, vals)

                cursor.execute('set GLOBAL max_allowed_packet=67108864')
                cursor.executemany(sql, tpls)
                connection.commit()
                return {
                    "message":"Data transferred successfully",
                    "status":"success"
                }

            except Exception as e:
                connection.rollback()
                raise e

            finally:
                cursor.close()
                connection.close()
        else:
            return {'status': 'error', 'message': 'Failed to connect to the database'}

