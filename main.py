from . import users


def main():
    users.Guest().check_both()
    users.Admin("").modify_room()
    print("I am main")
    pass


if __name__ == "__main__":
    main()
