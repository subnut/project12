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
