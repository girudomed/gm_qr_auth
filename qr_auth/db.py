import psycopg2
from psycopg2.extras import RealDictCursor

from . import config


def get_connection():
    return psycopg2.connect(config.DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id serial PRIMARY KEY,
                    telegram_id bigint UNIQUE,
                    full_name text NOT NULL,
                    phone text,
                    confirmed boolean DEFAULT false
                );
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS attendances (
                    id serial PRIMARY KEY,
                    user_id bigint REFERENCES users(id),
                    action text NOT NULL,
                    ts timestamptz DEFAULT now()
                );
                """
            )
            conn.commit()


def record_event(user_id: int, action: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO attendances (user_id, action) VALUES (%s, %s)",
                (user_id, action),
            )
            conn.commit()
