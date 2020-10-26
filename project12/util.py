import mysql.connector
from typing import List, Union
from project12 import userinput
from project12.constants import DATABASE_SERVER, DATABASE_NAME, GUEST_USERNAME
from project12.tabulate import tabulate


class Check:
    def __init__(self):
        pass

    def server(self, *args) -> bool:
        try:
            mysql.connector.connect(
                user=GUEST_USERNAME,
                host=DATABASE_SERVER,
            )
        except:
            print(
                f"""Cannot connect to server using username '{GUEST_USERNAME}'.
Please check the connection."""
            )
            return False
        else:
            return True

    def database(self, *args) -> bool:
        if not self.server():
            return False
        try:
            mysql.connector.connect(
                user=GUEST_USERNAME,
                host=DATABASE_SERVER,
                database=DATABASE_NAME,
            )
        except:
            print("Database not found. Please create the database.")
            return False
        else:
            return True

    def password(self, username, password) -> bool:
        if not self.server():
            return False
        try:
            mysql.connector.connect(
                user=username,
                password=password,
                host=DATABASE_SERVER,
                database=DATABASE_NAME,
            )
        except:
            print("Password incorrect. Please try again.")
            return False
        else:
            return True


class Cursor:
    def __init__(self, outer_connection):
        self.connection = outer_connection
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


class Select:
    def __init__(self):
        if Check().database():
            self.connection = mysql.connector.connect(
                user=GUEST_USERNAME,
                host=DATABASE_SERVER,
                database=DATABASE_NAME,
            )

    def _cursor(self):
        return Cursor(self.connection)

    def room_number(self, prompt="Please enter the room number: ") -> Union[int, None]:
        with self._cursor() as cursor:
            cursor.execute("select `room number` from `rooms`;")
            rooms = cursor.fetchall()
            rooms = [z for (z,) in rooms]
        while True:
            room = input(prompt)
            if not (room.isdigit() and int(room) in rooms):
                if not userinput.yes_or_no("Invalid room number. Try again?"):
                    return None
            else:
                break
        return int(room)

    def room_type(self, prompt="Please enter the room type: ") -> Union[int, None]:
        with self._cursor() as cursor:
            cursor.execute("select `room type` from `rates`;")
            room_types = cursor.fetchall()
            room_types = [z for (z,) in room_types]
        while True:
            room_type = input(prompt)
            if not (room_type.isdigit() and int(room_type) in room_types):
                if not userinput.yes_or_no("Invalid room type. Try again?"):
                    return None
            else:
                break
        return int(room_type)


class Lister:
    def __init__(self):
        if Check().database():
            self.connection = mysql.connector.connect(
                user=GUEST_USERNAME,
                host=DATABASE_SERVER,
                database=DATABASE_NAME,
            )

    def _cursor(self):
        return Cursor(self.connection)

    def room_numbers(self) -> List[int]:
        with self._cursor() as cursor:
            cursor.execute("select `room number` from `rooms`;")
            room_numbers = cursor.fetchall()
            room_numbers = [z for (z,) in room_numbers]
            return room_numbers

    def room_types(self) -> List[int]:
        with self._cursor() as cursor:
            cursor.execute("select `room type` from `rates`;")
            room_types = cursor.fetchall()
            room_types = [z for (z,) in room_types]
            return room_types

    def room_types_being_used(self) -> List[int]:
        with self._cursor() as cursor:
            cursor.execute("select unique (`room type`) from `rooms`;")
            room_types = cursor.fetchall()
            room_types = [z for (z,) in room_types]
            return room_types


def print_table(data):
    raw = tabulate.tabulate(data, headers="firstrow", tablefmt="orgtbl")
    sep = "+" + ("-" * (len(raw.split("\n")[0]) - 2)) + "+"
    print(sep, raw, sep, sep="\n")
