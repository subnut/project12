### Files

#### Directory Stucture
```
.
├── project12
│   ├── constants.py
│   ├── __init__.py
│   ├── __main__.py
│   ├── tabulate
│   ├── userinput.py
│   ├── users.py
│   └── util.py
├── README.md.botify
├── run.py
└── sql_commands.sql
```


##### `sql_commands.sql`

```sql
create database `hotel database`;
use `hotel database`;

create table `rates` (
`room type` int (3) primary key,
`beds` int(2) not null,
`AC` bool NOT NULL DEFAULT FALSE,
`rate` int(7) not null,
check (`AC` between 0 and 1) -- bool defaults to tinyint(1) which can also be 2,3 etc.
);

/*
 We use constraint on rooms rather than types because you
 should not have rooms without types, but you may want to upgrade
 some of the existing rooms to a new type
*/

create table `rooms` (
`room number` int (6) primary key,
`room type` int (3),
`occupied` bool NOT NULL default False,
foreign key (`room type`) references `rates` (`room type`) -- since the manager can add new room types anytime he/she wants, but not the other way round
ON UPDATE CASCADE ON DELETE RESTRICT
);

create user 'guest'@'localhost';
revoke all on *.* from 'guest'@'localhost';
grant select on `hotel database` . `rates` to 'guest'@'localhost';
grant select(`room number`), select(`room type`), select(`occupied`) on `hotel database` . `rooms` to 'guest'@'localhost';

create user 'manager'@'localhost';
revoke all on *.* from 'manager'@'localhost';
grant all on `hotel database` . * to 'manager'@'localhost' with grant option;



-- vim: et
```

##### `run.py`

```python
from project12 import __main__
```

##### `project12/__init__.py`

```python
from project12 import __main__
```

##### `project12/__main__.py`

```python
import os
import readline
from sys import exit
from project12 import users
from project12.constants import HOTEL_NAME, ADMIN_USERNAME
from project12.userinput import choose_option, get_password, yes_or_no
from project12.util import Check, Logout


def _clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def _helper(user_object):
    _clear_screen()
    while True:
        print("Welcome!")
        print()
        print("What would you like to do?")
        try:
            user_object.functions[choose_option(user_object.actions)]()
        except EOFError as E:
            if not isinstance(E, Logout):
                print()
            if yes_or_no("Do you want to logout?"):
                break
            _clear_screen()
        except KeyboardInterrupt:
            print()
            exit(0)


def main():
    while True:
        _clear_screen()
        print("WELCOME TO", HOTEL_NAME)
        print()
        print("You are:")
        option = choose_option(("Guest", "Manager"))
        if option:
            while True:
                try:
                    password = get_password()
                except (EOFError, KeyboardInterrupt):
                    if yes_or_no("Do you want to logout?"):
                        print()
                        break
                if Check().password(ADMIN_USERNAME, password):
                    user_object = users.Admin(password)
                    _helper(user_object)
                    break
                else:
                    if not yes_or_no("Try again?"):
                        break
        else:
            user_object = users.Guest()
            _helper(user_object)


if Check().database():
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print()
        exit(0)
else:
    exit(1)
```

##### `project12/constants.py`

```python
DATABASE_SERVER = "localhost"
DATABASE_NAME = "hotel database"
GUEST_USERNAME = "guest"
LOGIN_MANAGER = "loginuser"
ADMIN_USERNAME = "manager"
HOTEL_NAME = "THE GRAND HOTEL"
```

##### `project12/users.py`

```python
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
                if userinput.yes_or_no("Room already exists. Try again?"):
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
```

##### `project12/util.py`

```python
import sys
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
        except mysql.connector.errors.InterfaceError as exception:
            print(exception)
            print("Please check the connection.")
            sys.exit(1)
        except mysql.connector.errors.ProgrammingError as exception:
            print(exception)
            print(
                f"GUEST_USERNAME not configured properly.\n\
Please check whether user '{GUEST_USERNAME}' exists, \
or set GUEST_USERNAME to the correct username."
            )
            sys.exit(1)
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
        except mysql.connector.errors.ProgrammingError as exception:
            print(exception)
            print(
                "Database not configured properly. \
Please create the database as advised, and set proper permissions to access it."
            )
            sys.exit(1)
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
        except mysql.connector.errors.ProgrammingError:
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


class Logout(EOFError):
    pass


def print_table(data):
    raw = tabulate.tabulate(data, headers="firstrow", tablefmt="orgtbl")
    sep = "+" + ("-" * (len(raw.split("\n")[0]) - 2)) + "+"
    print(sep, raw, sep, sep="\n")
```

##### `project12/userinput.py`

```python
"""A module to take input from user
Functions available -
  - choose_option(options: Union[List, Tuple]) -> int
        Shows options passed to it and asks the user to select one option.
        Returns the index of the selected option.
        :param options Union[List, Tuple]: Options to show to user
        :rtype int: Index of option selected by user
        :raises RuntimeError: param 'options' is of wrong type
  - yes_or_no(confirmation_text: str) -> bool
        Prints 'confirmation_text [Y/n] ' and waits for user input.
        On user input, check for 'y' or 'n' in the input. If no input, default to 'y'
        :param confirmation_text str: Text to be shown to the user, including the '?'
        :rtype bool: True if 'y' or no input, else False
  - get_password(text: Optional[str]=None) -> str
        Take password from user
        :param text Optional[str]: Prompt to show to user, 'Password:' by default
        :rtype str: Password input by user
  - input_int(text: Optional[str] = "Please enter: ") -> Union[int, None]
        Takes integer input from user and returns it. Else returns None.
        :param text Optional[str]: Prompt to show user
        :rtype Union[int, None]: If no input, None. Else return int(user_input)
"""
import getpass
from typing import Optional, Union, List, Tuple


def choose_option(options: Union[List, Tuple]) -> int:
    """
    Shows options passed to it and asks the user to select one option.
    Returns the index of the selected option.

    :param options Union[List, Tuple]: Options to show to user
    :rtype int: Index of option selected by user
    :raises RuntimeError: param 'options' is of wrong type
    """
    if not isinstance(options, (list, tuple)):
        raise RuntimeError("choose_option() expects list or tuple as input")
    for (index, option) in enumerate(options):
        print(str(index + 1) + ": " + str(option))
    while True:
        user_input = input(f"Choose your option (1-{len(options)}): ")
        if user_input.isdigit() and (1 <= int(user_input) <= len(options)):
            return int(user_input) - 1
        else:
            print("Invalid input. Please try again.")


def yes_or_no(confirmation_text: str) -> bool:
    """
    Prints 'confirmation_text [Y/n] ' and waits for user input.
    On user input, check for 'y' or 'n' in the input. If no input, default to 'y'

    :param confirmation_text str: Text to be shown to the user, including the '?'
    :rtype bool: True if 'y' or no input, else False
    """
    while True:
        user_input = input(confirmation_text + " [Y/n] ")
        user_input = user_input.lower()
        if user_input == "":
            return True
        elif user_input in "yes" and user_input.startswith("y"):
            return True
        elif user_input in "no" and user_input.startswith("n"):
            return False
        else:
            print("Invalid input. Please try again.")


def get_password(text: Optional[str] = None) -> str:
    """
    Take password from user

    :param text Optional[str]: Prompt to show to user, 'Password:' by default
    :rtype str: Password input by user
    """
    if text is not None:
        return getpass.getpass(prompt=text)
    else:
        return getpass.getpass()


def input_int(text: Optional[str] = "Please enter: ") -> Union[int, None]:
    """
    Takes integer input from user and returns it. Else returns None.

    :param text Optional[str]: Prompt to show user
    :rtype Union[int, None]: If no input, None. Else return int(user_input)
    """
    while True:
        user_input = input(text)
        if not user_input.isdigit():
            if not yes_or_no("Invalid input. Try again?"):
                return None
        else:
            return int(user_input)
```


<!--
vim: ft=markdown
-->

