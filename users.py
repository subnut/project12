import mysql.connector
import tabulate
from constants import GUEST_USERNAME, DATABASE_NAME, DATABASE_SERVER, ADMIN_USERNAME
import userinput

# from userinput import *


class Guest:
    def __init__(self):
        self.connector = mysql.connector.connect(
            user=GUEST_USERNAME,
            host=DATABASE_SERVER,
            database=DATABASE_NAME,
        )
        self.actions = ("Check empty rooms", "Check rates", "Check both")
        self.functions = (self.check_rooms, self.check_rates, self.check_both)

    def check_rooms(self):
        with self.connector.cursor() as cursor:
            rows = cursor.execute(
                "select `room number`, `room type` from `rooms` order by `room number`;"
            )
            data = cursor.fetchall()
        if rows == 0:
            print("No empty rooms available right now. Please check again later.")
        else:
            data = ("Room no.", "Room type") + data
            print(tabulate.tabulate(data))

    def check_rates(self):
        with self.connector.cursor() as cursor:
            cursor.execute(
                "select `room type`, `beds`, `AC`, `rate` from `rates` order by `room type`;"
            )
            data = cursor.fetchall()
        data = ("Room type", "Beds", "Air-conditioned", "Rate per day") + data
        print(tabulate.tabulate(data))

    def check_both(self):
        with self.connector.cursor() as cursor:
            rows = cursor.execute(
                "select `room number`, `beds`, `AC`, `rate` \
                from `rooms`, `rates` where `rooms`.`room type` = `rates`.`room type` \
                order by `room number`;"
            )
            data = cursor.fetchall()
        if rows == 0:
            print("No empty rooms available right now. Please check again later.")
        else:
            data = ("Room no.", "Beds", "Air-conditioned", "Rate per day") + data
            print(tabulate.tabulate(data))


class Tenant:
    def __init__(self, user, password):
        self.user = user
        self.connector = mysql.connector.connect(
            user=user,
            password=password,
            host=DATABASE_SERVER,
            database=DATABASE_NAME,
            autocommit=True,
            # cursorclass=mysql.connector.cursors.DictCursor,
        )
        self.actions = ("Show details", "Edit details", "Print payslip")
        self.functions = [self.print_details, self.edit_details, self.payslip]

    def print_details(self):
        pass

    def edit_details(self):
        pass

    def payslip(self):
        pass


class Admin:
    def __init__(self, password):
        self.connector = mysql.connector.connect(
            user=ADMIN_USERNAME,
            password=password,
            host=DATABASE_SERVER,
            database=DATABASE_NAME,
            autocommit=True,
            # cursorclass=mysql.connector.cursors.Cursor,
        )
        self.actions = (
            "Add new room",
            "Add room type",
            "Modify rooms",
            "Modify room type",
            "Change room status",
        )
        self.functions = [
            self.add_room,
            self.add_room_type,
            self.modify_room,
            self.modify_room_type,
            self.change_status,
        ]

    def add_room(self):
        return None

    def add_room_type(self):
        return None

    def modify_room(self):
        return None

    def modify_room_type(self):
        return None

    def change_status(self):
        # with self.connector.cursor() as cursor:
        #     cursor.execute("select `room number` from `rooms`;")
        #     rooms = cursor.fetchall()
        #     rooms = [z for (z,) in rooms]
        cursor = self.connector.cursor()
        cursor.execute("select `room number` from `rooms`;")
        rooms = cursor.fetchall()
        rooms = [z for (z,) in rooms]
        cursor.close()
        while True:
            room_to_change = input("Please enter the room number: ")
            if not (room_to_change.isdigit() and int(room_to_change) in rooms):
                if not userinput.yes_or_no("Invalid room number. Try again?"):
                    return
            else:
                break
        # with self.connector.cursor() as cursor:
        #     cursor.execute(
        #         """UPDATE `rooms`
        #         set `occupied` = (`occupied` + 1) % 2
        #         where `room number` = %s;""",
        #         (room_to_change,),
        #     )
        cursor = self.connector.cursor()
        cursor.execute(
            """UPDATE `rooms`
            set `occupied` = (`occupied` + 1) % 2
            where `room number` = %s""",
            (str(room_to_change),),
        )
        cursor.close()
