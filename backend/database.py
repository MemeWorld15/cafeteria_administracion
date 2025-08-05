import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    return psycopg2.connect(
        host="https://e548793ec54c.ngrok-free.app",  # Host
        user="postgres",   # Usuario
        password="2612",   # Contraseña
        database="cafe_admin",  # Base de datos
        port="5432"  # Puerto
    )
