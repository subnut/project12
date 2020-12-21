import mysql.connector
from project12.constants import (
    GUEST_USERNAME,
    DATABASE_NAME,
    DATABASE_SERVER,
    ADMIN_USERNAME,
)
from project12 import userinput
from project12 import util
from project12.util import Logout

checker = util.Check()
selecter = util.Select()
lister = util.Lister()


class Guest:
    def __init__(self):
        if checker.database():
            self.connection = mysql.connector.connect(
                user=GUEST_USERNAME,
                host=DATABASE_SERVER,
                database=DATABASE_NAME,
            )
        self.actions = ("Check empty rooms", "Check rates", "Check both", "Logout")
        self.functions = (
            self.check_rooms,
            self.check_rates,
            self.check_both,
            self._logout,
        )

    def _logout(self):
        raise Logout

    def _cursor(self):
        return util.Cursor(self.connection)

    def check_rooms(self):
        with self._cursor() as cursor:
            cursor.execute(
                "select `room number`, `room type` from `rooms` \
                where `occupied` = 0 order by `room number`;"
            )
            rows = cursor.rowcount
            data = cursor.fetchall()
        if (rows == 0) or (len(data) == 0):
            print("No empty rooms available right now. Please check again later.")
        else:
            data = [("Room no.", "Room type")] + data
            util.print_table(data)

    def check_rates(self):
        with self._cursor() as cursor:
            cursor.execute(
                "select `room type`, `beds`, `AC`, `rate`\
                from `rates` order by `room type`;"
            )
            data = cursor.fetchall()
            rows = cursor.rowcount
        if (rows == 0) or (len(data) == 0):
            print("No rates available. Please contact the Hotel Manager.")
        else:
            data = [("Room type", "Beds", "AC", "Rate per day")] + data
            util.print_table(data)

    def check_both(self):
        with self._cursor() as cursor:
            cursor.execute(
                "select `room number`, `beds`, `AC`, `rate` \
                from `rooms`, `rates` where `occupied` = 0 and \
                `rooms`.`room type` = `rates`.`room type` \
                order by `room number`;"
            )
            data = cursor.fetchall()
            rows = cursor.rowcount
        if (rows == 0) or (len(data) == 0):
            print("No empty rooms available right now. Please check again later.")
        else:
            data = [("Room no.", "Beds", "AC", "Rate per day")] + data
            util.print_table(data)


class Admin:
    def __init__(self, password):
        if checker.database() and checker.password(ADMIN_USERNAME, password):
            self.connection = mysql.connector.connect(
                user=ADMIN_USERNAME,
                password=password,
                host=DATABASE_SERVER,
                database=DATABASE_NAME,
            )
        self.actions = (
            "Show rooms",
            "Show room types",
            "Add new room",
            "Add room type",
            "Modify room",
            "Modify room type",
            "Delete room",
            "Delete room type",
            "Change room status",
            "Logout",
        )
        self.functions = [
            self.show_rooms,
            self.show_room_types,
            self.add_room,
            self.add_room_type,
            self.modify_room,
            self.modify_room_type,
            self.delete_room,
            self.delete_room_type,
            self.change_status,
            self._logout,
        ]

    def _logout(self):
        raise Logout

    def _cursor(self):
        return util.Cursor(self.connection)

    def show_rooms(self):
        with self._cursor() as cursor:
            cursor.execute(
                "select `room number`, `room type`, `occupied` \
                from `rooms` order by `room number`;"
            )
            rows = cursor.rowcount
            data = cursor.fetchall()
        if (rows == 0) or (len(data) == 0):
            print("No room has been added till now.")
        else:
            data = [("Room no.", "Room type", "Occupied")] + data
            util.print_table(data)

    def show_room_types(self):
        with self._cursor() as cursor:
            cursor.execute(
                "select `room type`, `beds`, `AC`, `rate`\
                from `rates` order by `room type`;"
            )
            rows = cursor.rowcount
            data = cursor.fetchall()
        if (rows == 0) or (len(data) == 0):
            print("No room type has been added till now.")
        else:
            data = [("Room type", "Beds", "AC", "Rate per day")] + data
            util.print_table(data)

    def add_room(self):
        while True:
            room_number = userinput.input_int("Enter the new room number: ")
            if room_number is None:
                return
            if room_number in lister.room_numbers():
                if userinput.yes_or_no("Room already exists. Try again?"):
                    continue
                else:
                    return
            else:
                break
        self.show_room_types()
        room_type = selecter.room_type("Enter the room type: ")
        if room_type is None:
            return
        with self._cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO `rooms` (`room number`, `room type`)
                           VALUES ('{room_number}','{room_type}');"""
            )

    def add_room_type(self):
        while True:
            room_type = userinput.input_int("Enter the new room type: ")
            if room_type is None:
                return
            if room_type in lister.room_types():
                if userinput.yes_or_no("Room type already exists. Try again?"):
                    continue
                else:
                    return
            else:
                break
        values_to_insert = [room_type]
        beds = userinput.input_int("Enter the number of beds: ")
        if beds is None:
            return
        ac = int(userinput.yes_or_no("AC available?"))
        if ac is None:
            return
        rate = userinput.input_int("Enter the rate: ")
        if rate is None:
            return
        values_to_insert += [beds, ac, rate]
        values_to_insert = tuple(values_to_insert)
        with self._cursor() as cursor:
            cursor.execute(
                "insert into `rates` (`room type`, `beds`, `AC`, `rate`)\
                           values (%s, %s, %s, %s);",
                values_to_insert,
            )

    def modify_room(self):
        room_number = selecter.room_number("Enter room number: ")
        if room_number is None:
            return
        room_type = selecter.room_type("Enter room type: ")
        if room_type is None:
            return
        with self._cursor() as cursor:
            cursor.execute(
                f"""UPDATE `rooms`
                           SET `room type`='{room_type}'
                           WHERE `room number`='{room_number}';"""
            )

    def modify_room_type(self):
        room_type = selecter.room_type("Enter the room type to change: ")
        if room_type is None:
            return
        for param in ("beds", "AC", "rate"):
            with self._cursor() as cursor:
                cursor.execute(
                    f"select `{param}` from `rates`\
                               where `room type` = '{room_type}'"
                )
                old_value = cursor.fetchall()[0][0]
            if param == "AC":
                print(param, "is", ["not ", ""][bool(old_value)] + "available")
                new_value = None
                if userinput.yes_or_no("Do you want to change it?"):
                    new_value = int(userinput.yes_or_no("AC available now?"))
            else:
                print(param, "is", old_value)
                new_value = None
                if userinput.yes_or_no("Do you want to change it?"):
                    new_value = userinput.input_int("Enter the new value: ")
            if new_value is not None:
                with self._cursor() as cursor:
                    cursor.execute(
                        f"update `rates`\
                                   set `{param}` = '{new_value}' \
                                   where `room type` = '{room_type}'"
                    )

    def delete_room(self):
        room = selecter.room_number("Enter the room number to be deleted: ")
        if room is not None:
            print(f"Room {room} shall be deleted.")
            if userinput.yes_or_no("Are you sure?"):
                with self._cursor() as cursor:
                    cursor.execute(
                        f"DELETE FROM `rooms` WHERE `room number` = '{room}'"
                    )

    def delete_room_type(self):
        room_type = selecter.room_type("Enter the room type to be deleted: ")
        if room_type is not None:
            if room_type in lister.room_types_being_used():
                print(
                    "Before deleting room type, please remove or modify all rooms associated with it."
                )
                return
            else:
                print(f"Room type {room_type} shall be deleted.")
                if userinput.yes_or_no("Are you sure?"):
                    with self._cursor() as cursor:
                        cursor.execute(
                            f"DELETE FROM `rates` WHERE `room type` = '{room_type}'"
                        )

    def change_status(self):
        room_to_change = selecter.room_number()
        if room_to_change is not None:
            with self._cursor() as cursor:
                cursor.execute(
                    """UPDATE `rooms`
                    set `occupied` = (`occupied` + 1) % 2
                    where `room number` = %s;""",
                    (room_to_change,),
                )
