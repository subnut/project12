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
        user_input = input("Choose your option: ")
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
        print(confirmation_text + " [Y/n] ", end="")
        user_input = input()
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
