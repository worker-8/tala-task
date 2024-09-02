from database.connection import create_sqlite3_conn

from .uow import UnitOfWork

def create_uow() -> UnitOfWork:
    return UnitOfWork(create_sqlite3_conn)