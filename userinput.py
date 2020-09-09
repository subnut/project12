def choose_option(options):
    """
    Choose an option
    from a supplied list/tuple of it

    :param options list/tuple: options to choose from
    """
    if not isinstance(options, (list, tuple)):
        raise RuntimeError("choose_option() expects list or tuple as input")
    for index in range(len(options)):
        print(str(index + 1) + ": " + str(options[index]))
    while True:
        user_input = input("Choose your option: ")
        if user_input.isdigit() and (1 <= int(user_input) <= len(options)):
            return int(user_input) - 1
        else:
            print("Invalid input. Please try again.")


def yes_or_no(confirmation_text):
    """
    Prints 'confirmation_text [Y/n] ' and waits for user input
    On user input, checks for y or n
    and returns True or False accordingly

    :param confirmation_text str: confirmation_text including the '?'
    """
    while True:
        print(confirmation_text + " [Y/n] ", end="")
        user_input = input()
        user_input = user_input.lower()
        if user_input == "":
            print("Y")
            return True
        elif user_input in "yes" and user_input.startswith("y"):
            return True
        elif user_input in "no" and user_input.startswith("n"):
            return False
        else:
            print("Invalid input. Please try again.")
