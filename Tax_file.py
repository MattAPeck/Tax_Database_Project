import datetime
import pytz
from connections import get_connection
import database


class Return:
    def __init__(self, status: str, client_id: int, cpa_id: int, time_filed: float, cpa_checked: str,
                 return_number: int = None,):
        self.return_number = return_number
        self.status = status
        self.time_filed = time_filed
        self.cpa_checked = cpa_checked
        self.client_id = client_id
        self.cpa_id = cpa_id

    def save(self):
        with get_connection() as connection:
            tax_return = database.create_return_info(connection, self.status, self.client_id, self.cpa_id,
                                                     self.time_filed, self.cpa_checked)
            self.return_number = tax_return

    @classmethod
    def get(cls, return_number: int):
        with get_connection() as connection:
            Return = database.check_status(connection, return_number)
            return Return

    def mark_return(self, return_number):
        with get_connection() as connection:
            mark = database.mark_return(connection, return_number)
            return mark

    def check(self, return_number):
        with get_connection() as connection:
            status = database.check_status(connection, return_number)
            return status

    def file(self):
        with get_connection() as connection:
            current_datetime_utc = datetime.datetime.now(tz=pytz.utc)
            current_timestamp = current_datetime_utc.timestamp()
            status = 'filed'
            file = database.file_return(connection, status, current_timestamp, self.return_number)
            return file