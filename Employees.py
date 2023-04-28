import database
from connections import get_connection


class Employee:
    def __init__(self, name: str, phone_number: str, employee_type: str = None, _id: int = None):
        self.id = _id
        self.name = name
        self.phone_number = phone_number
        self.employee_type = employee_type

    def save(self):
        with get_connection() as connection:
            new_employee_id = database.create_employee(connection, self.name, self.phone_number, self.employee_type)
            self.id = new_employee_id

    @classmethod
    def get_cpa(cls):
        with get_connection() as connection:
            cpas = database.get_cpa(connection)
            return cpas

    @classmethod
    def get_all(cls):
        with get_connection() as connection:
            employees = database.get_all_employees(connection)
            return employees
