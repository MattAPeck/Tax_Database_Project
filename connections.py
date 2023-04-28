from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager

# I just straight up provided the Database URL for this project. I couldn't figure out how to get .env file working.

database_url = 'postgres://mqakozis:NQk6YDcpjBtbaDpaeJkgk2dpycTQXt7Y@jelani.db.elephantsql.com/mqakozis'
if not database_url:
    print('Please enter a correct database url')

pool = SimpleConnectionPool(minconn=1, maxconn=10, dsn=database_url)


@contextmanager
def get_connection():
    connection = pool.getconn()

    try:
        yield connection
    finally:
        pool.putconn(connection)
