import psycopg2
from environs import Env

env = Env()
env.read_env()


def get_db_connection():
    return psycopg2.connect(
        dbname=env.str("PG_DB"),
        user=env.str("PG_USER"),
        password=env.str("PG_PASSWORD"),
        host=env.str("PG_HOST"),
        port=env.str("PG_PORT"),
    )
