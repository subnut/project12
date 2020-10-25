from . import users
from .constants import HOTEL_NAME, ADMIN_USERNAME
from .userinput import choose_option, get_password, yes_or_no
from .util import Check
from sys import exit
import os


def _clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def _helper(user_object):
    _clear_screen()
    print("Welcome!")
    while True:
        print()
        print("What would you like to do?")
        try:
            user_object.functions[choose_option(user_object.actions)]()
        except EOFError:
            if yes_or_no("Do you want to logout?"):
                break
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
                        continue
                if Check().password(ADMIN_USERNAME, password):
                    user_object = users.Admin(password)
                    _helper(user_object)
                else:
                    if not yes_or_no("Try again?"):
                        break
        else:
            user_object = users.Guest()
            _helper(user_object)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print()
        exit(0)
