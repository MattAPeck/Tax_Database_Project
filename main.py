import database
from Employees import Employee
from client import Client
from connections import get_connection
from Tax_file import Return
import datetime
import pytz


MENU_PROMPT = """--Menu--

1. Add Client
2. Add employee
3. Assign CPA to client
4. Check client materials
5. Mark client provided materials
6. Check return status
7. File a tax return
8. Check if CPA checked return
9. Mark a return CPA checked
10. Create a Tax Return
11. Exit

Enter your choice: """


# Adds clients to the client table. I have it recommended that you give the client a CPA with an ID of 0 to start.
# Now, there is no individual with an ID of 0, but it is temporary until we use the assign function to actually give
# them a CPA.

def prompt_add_client():
    client_name = input("Enter Client Name: ")
    client_address = input("Enter Client Address: ")
    client_income = input("Enter Client Income: ")
    client_cpa = int(input("Enter id of CPA (just input 0 if not assigned one): "))
    client_materials = input("Has Client provided tax materials: ")
    client = Client(client_name, client_address, client_income, client_cpa, client_materials)
    client.save()

# Puts employees into the table, and you specify if it is a CPA or assistant here. I have the SQL set up so that later,
# when you go to assign a CPA, it will only show you employees with CPA in the type.


def prompt_add_employee():
    employee_type = input("Is this Employee a CPA or Assistant: ")
    employee_name = input("Name of new Employee: ")
    employee_phone = input("What is the Employee's Phone Number: ")
    employee = Employee(employee_name, employee_phone, employee_type)
    employee.save()
    employee_list = Employee.get_all()
    print(employee_list)

# See, the first print function is supposed to print out a list of CPA's, and I had it working, but it stopped working
# during testing and I'm not sure why or how to fix it.
# I swear I had all of these just about working,
# but now I get the same error over and over "IndexError: tuple index out of range"


def assign_cpa():
    cpas = Employee.get_cpa()
    print(cpas)
    cpa_id = int(input("Please input the id of the cpa you would like to assign: "))
    clients = Client.get_all()
    print(clients)
    client_id = int(input("Please select the id of the client you would like to assign the CPA to: "))
    c = Client.get(client_id)
    assigned_client = c.assign(cpa_id)
    assigned_client.save()

# This one is working luckily.


def check_materials():
    clients = Client.get_all()
    print(clients)
    client_id = int(input("Enter the id of the client: "))
    c = Client.get(client_id)
    client = c.check_materials(client_id)
    print(client)

# This one gives me a TypeError: str object is not callable
def mark_materials():
    clients = Client.get_all()
    print(clients)
    client_id = int(input("Enter the id of the client who has provided their materials: "))
    c = Client.get(client_id)
    client = c.materials(client_id)
    client.save()


# Now this one is giving me an AttributeError: 'tuple' object has no attribute 'check

def check_return_status():
    return_number = int(input("Enter the return number: "))
    r = Return.get(return_number)
    status = r.check(return_number)
    print(status)


def file_return():
    return_number = int(input("Enter the number of the tax return you would like to file: "))
    r = Return.get(return_number)
    file = r.file(return_number)
    file.save()

# I can't figure out why I'm getting errors with all of my File statements, I hope you can figure it out.


def check_if_checked():
    return_number = int(input("Enter the number of the return you would like to see if is CPA checked: "))
    r = Return.get(return_number)
    check = r.check(return_number)
    check.save()


def mark_return():
    return_number = int(input("Enter the tax return number you would like to mark checked by a CPA: "))
    r = Return.get(return_number)
    mark = r.mark_return(return_number)
    mark.save()


def create_return():
    status = input("Are you filing the return now?: ")
    if status == 'Y':
        status = 'Filed'
        current_datetime_utc = datetime.datetime.now(tz=pytz.utc)
        time_stamp = current_datetime_utc.timestamp()
    else:
        status = 'Not Filed'
        time_stamp = 0
    checked = 'Not checked'
    client_id = int(input("Enter the id of the client this return is for: "))
    cpa_id = int(input("Enter the id of the CPA assigned to the client: "))
    tax_return = Return(status, client_id, cpa_id, time_stamp, checked)
    tax_return.save()


MENU_OPTIONS = {
    "1": prompt_add_client,
    "2": prompt_add_employee,
    "3": assign_cpa,
    "4": check_materials,
    "5": mark_materials,
    "6": check_return_status,
    "7": file_return,
    "8": check_if_checked,
    "9": mark_return,
    "10": create_return
}


def menu():
    with get_connection() as connection:
        database.create_tables(connection)
        while (selection := input(MENU_PROMPT)) != "11":
            try:
                MENU_OPTIONS[selection]()
            except KeyError:
                print("Invalid input selected. Please try again.")


if __name__ == "__main__":
    menu()
