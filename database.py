from contextlib import contextmanager

CREATE_EMPLOYEE = """CREATE TABLE IF NOT EXISTS employees
(employee_id SERIAL PRIMARY KEY, name TEXT, phone_number TEXT, employee_type TEXT);"""

CREATE_CLIENT = """CREATE TABLE IF NOT EXISTS clients
(client_id SERIAL PRIMARY KEY, name TEXT, address TEXT, income TEXT, 
materials TEXT, cpa_id INTEGER);"""

CREATE_TAX_INFO = """CREATE TABLE IF NOT EXISTS tax_info
(return_number SERIAL PRIMARY KEY, status TEXT, client_id INTEGER, cpa_id INTEGER, time_filed INTEGER, cpa_checked TEXT,
FOREIGN KEY (client_id) REFERENCES clients(client_id), 
FOREIGN KEY (cpa_id) REFERENCES employees(employee_id)); """

#--- selection queries ---

SELECT_CLIENT = "SELECT * FROM clients WHERE client_id = %s;"
SELECT_EMPLOYEE = "SELECT FROM employees WHERE employee_id = %s;"
SELECT_ALL_EMPLOYEES = "SELECT * FROM employees;"
SELECT_CPAS = "SELECT * FROM employees WHERE employee_type LIKE 'c%';"
SELECT_CLIENT_MATERIALS = "SELECT materials FROM clients WHERE client_id = %s;"
SELECT_ALL_CLIENTS = "SELECT * FROM clients;"
SELECT_RETURN = "SELECT FROM tax_info WHERE client_id = %s;"


#--- insertion queries ---

INSERT_EMPLOYEES = "INSERT INTO employees (name, phone_number, employee_type) " \
                   "VALUES (%s, %s, %s) RETURNING employee_id;"
INSERT_CLIENT = """INSERT INTO clients (name, address, income, cpa_id, materials)
VALUES (%s, %s, %s, %s, %s) RETURNING client_id;"""
INSERT_TAX_INFO = """INSERT INTO tax_info (status, client_id, cpa_id, time_filed, cpa_checked)
 VALUES (%s, %s, %s, %s, %s) RETURNING return_number;"""
FILE_TAX = """UPDATE tax_info SET status = %s, time_filed = %s, WHERE return_number = %s;"""
ASSIGN_CPA = """UPDATE clients SET cpa_id = %s WHERE client_id = %s;"""
PROVIDE_MATERIALS = """UPDATE clients SET materials = 'Provided' WHERE client_id = %s;"""
MARK_RETURN = """UPDATE tax_info SET cpa_checked = 'Checked' WHERE return_number = %s;"""


@contextmanager
def get_cursor(connection):
    with connection:
        with connection.cursor() as cursor:
            yield cursor


def create_tables(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(CREATE_EMPLOYEE)
        cursor.execute(CREATE_CLIENT)
        cursor.execute(CREATE_TAX_INFO)


def create_client(connection, name: str, address: str, income: str, cpa_id: int, materials: str):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_CLIENT, (name, address, income, cpa_id, materials))
        cursor.execute(SELECT_ALL_CLIENTS)
        return cursor.fetchall()


def get_client(connection, client_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_CLIENT, (client_id, ))
        return cursor.fetchone()


def get_all_clients(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_CLIENTS)
        return cursor.fetchall()


def create_employee(connection, name: str, phone_number: str, employee_type: str):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_EMPLOYEES, (name, phone_number, employee_type))
        employee_id = cursor.fetchall()
        return employee_id


def get_cpa(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_CPAS)
        cpas = cursor.fetchall()
        return cpas


def create_return_info(connection, status: str, client_id: int, cpa_id: int,
                       time_filed: float, cpa_checked: str):
    with get_cursor(connection) as cursor:
        cursor.execute(INSERT_TAX_INFO, (status, client_id, cpa_id, time_filed, cpa_checked))
        return_number = cursor.fetchall()
        return return_number


def file_return(connection, status: str, time_filed: float, return_number: int):
    with get_cursor(connection) as cursor:
        cursor.execute(FILE_TAX, (status, time_filed, return_number))
        return cursor.fetchone()


def check_status(connection, return_number: int):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_RETURN, (return_number, ))
        return cursor.fetchone()


def assign_cpa(connection, client_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(ASSIGN_CPA, (client_id, ))
        return cursor


def add_materials(connection, client_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(PROVIDE_MATERIALS, (client_id, ))
        return cursor.fetchone()


def check_client_materials(connection, client_id: int):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_CLIENT_MATERIALS, (client_id, ))
        return cursor.fetchone()


def mark_return(connection, return_number: int):
    with get_cursor(connection) as cursor:
        cursor.execute(MARK_RETURN, (return_number, ))


def get_all_employees(connection):
    with get_cursor(connection) as cursor:
        cursor.execute(SELECT_ALL_EMPLOYEES)
        return cursor.fetchall()
