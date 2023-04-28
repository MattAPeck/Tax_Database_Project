import database
from connections import get_connection


class Client:
    def __init__(self, name: str, address: str, income: str, cpa_id: int, materials: str,  client_id: int = None):
        self.id = client_id
        self.name = name
        self.address = address
        self.income = income
        self.cpa_id = cpa_id
        self.materials = materials

    def save(self):
        with get_connection() as connection:
            new_client_id = database.create_client(connection, self.name, self.address, self.income,
                                                   self.cpa_id, self.materials)
            self.id = new_client_id

    @classmethod
    def get(cls, client_id: int):
        with get_connection() as connection:
            client = database.get_client(connection, client_id)
            return cls(client[0], client[1], client[2], client[3], client[4])

    @classmethod
    def get_all(cls):
        with get_connection() as connection:
            clients = database.get_all_clients(connection)
            return clients

    def assign(self, client_id: int):
        with get_connection() as connection:
            assign = database.assign_cpa(connection, client_id)
            self.cpa_id = assign

    def materials(self, client_id):
        with get_connection() as connection:
            provide = database.add_materials(connection, client_id)
            self.materials = provide
            return provide

    def check_materials(self, client_id: int):
        with get_connection() as connection:
            database.check_client_materials(connection, client_id)
            return self.materials
