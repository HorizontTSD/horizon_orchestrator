import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2 import errors
from environs import Env
import logging

logging.basicConfig(level=logging.INFO)
env = Env()
env.read_env()

db_name = "companies"

try:
    conn = psycopg2.connect(
        host=env.str("PG_HOST"),
        database=env.str('PG_DB'),
        user=env.str("PG_USER"),
        password=env.str("PG_PASSWORD"),
        sslmode='disable'
        # sslrootcert=os.path.expanduser('~/.cloud-certs/root.crt')
        # sslrootcert="system"
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE {db_name};")
    logging.info(f"База данных '{db_name}' успешно создана.")

except errors.DuplicateDatabase:
    logging.warning(f"База данных '{db_name}' уже существует.")
except Exception as e:
    logging.error(f"Ошибка при создании базы данных '{db_name}': {e}")
finally:
    if 'cur' in locals():
        cur.close()
    if 'conn' in locals():
        conn.close()
