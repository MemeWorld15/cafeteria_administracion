import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    return psycopg2.connect(
        host="dpg-d294hrur433s73c77a4g-a.oregon-postgres.render.com",
        user="cafe_db_p24b_user",
        password="QLfOq62eY79yiYFUJ2GxBH2khuzif8G8",
        database="cafe_db_p24b",
        port=5432,
        cursor_factory=RealDictCursor
    )
