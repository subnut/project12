from constants import DATABASE_SERVER, DATABASE_NAME
import mysql.connector


class Check:
    def server(self, *args):
        try:
            mysql.connector.connect(
                host=DATABASE_SERVER,
            )
        except:
            print("Cannot connect to server. Please check the connection.")
            return False
        else:
            return True

    def database(self, *args):
        if not self.server():
            return False
        try:
            mysql.connector.connect(
                host=DATABASE_SERVER,
                database=DATABASE_NAME,
            )
        except:
            print("Database not found. Please create the database.")
            return False
        else:
            return True


class Cursor:
    def __init__(self, outer):
        self.connection = outer.connection
        self.cursor = self.connection.cursor()

    def __enter__(self):
        return self.cursor

    def __exit__(self, typ, val, traceback):
        self.cursor.close()
        if traceback is None:
            self.connection.commit()
            return True
        else:
            self.connection.rollback()
            return False
