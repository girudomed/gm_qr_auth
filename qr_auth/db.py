import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError

from . import config


def get_connection():
    try:
        return psycopg2.connect(
            config.DATABASE_URL,
            cursor_factory=RealDictCursor,
            connect_timeout=5,
        )
    except OperationalError as e:
        raise RuntimeError(
            "Failed to connect to the database. Check DATABASE_URL and network connectivity."
        ) from e


def init_db():
    try:
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
    except RuntimeError as e:
        print(e)

def record_event(user_id: int, action: str):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO attendances (user_id, action) VALUES (%s, %s)",
                (user_id, action),
            )
            conn.commit()
