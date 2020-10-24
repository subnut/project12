import pymysql
from constants import GUEST_USERNAME, DATABASE_NAME, DATABASE_SERVER


class Guest:
    def __init__(self):
        self.connector = pymysql.connect(
            user=GUEST_USERNAME,
            host=DATABASE_SERVER,
            database=DATABASE_NAME,
            cursor=pymysql.cursors.DictCursor,
        )
        self.actions = ("Check empty rooms", "Check rates")
        self.functions = (self.check_rooms, self.check_rates)

    def check_rooms(self):
        with self.connector.cursor() as cursor:
            _data = cursor.execute()
        return None

    def check_rates(self):
        return None


class Tenant:
    def __init__(self, user, password):
        self.user = user
        self.connector = pymysql.connect(
            user=user,
            password=password,
            host=DATABASE_SERVER,
            database=DATABASE_NAME,
            cursor=pymysql.cursors.DictCursor,
        )
        self.actions = ("Show details", "Edit details", "Print payslip")
        self.functions = [self.print_details, self.edit_details, self.payslip]

    def print_details(self):
        pass

    def edit_details(self):
        pass

    def payslip(self):
        pass
