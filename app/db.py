import contextlib
import psycopg2
from .settings import settings


@contextlib.contextmanager
def get_conn():
    conn = psycopg2.connect(settings.DB_DSN)
    try:
        yield conn
    finally:
        conn.close()
