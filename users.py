class Guest:
    import mysql.connector

    def __init__(self):
        self.mysql_connector = self.mysql.connector.connect(
            user="guest", host="localhost", database="employee database"
        )
        self.options = ""


class Employee:
    import mysql.connector

    def __init__(self, user, password):
        self.user = user
        self.db_connection = self.mysql.connector.connect(
            user=user, password=password, host="localhost", database="Employee Database"
        )
        self.actions = ("Show details", "Edit details", "Print payslip")

    def print_details(self):
        pass

    def edit_details(self):
        pass

    def payslip(self):
        pass
