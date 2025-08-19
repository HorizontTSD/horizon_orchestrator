import psycopg2
from environs import Env

env = Env()
env.read_env()


def get_db_connection():
    return psycopg2.connect(
        dbname=env.str("TS_DB"),
        user=env.str("TS_USER"),
        password=env.str("TS_PASSWORD"),
        host=env.str("TS_HOST"),
        port=env.str("TS_PORT"),
    )
