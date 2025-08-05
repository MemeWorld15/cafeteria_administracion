from fastapi import APIRouter
from database import get_db_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()

@router.get("/graficas/top-productos")
def top_productos():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
       SELECT op.nombre_producto, SUM(op.cantidad) AS total_pedidos
FROM orden_productos op
JOIN ordenes o ON op.orden_id = o.id
WHERE DATE(o.fecha AT TIME ZONE 'America/Mexico_City') = CURRENT_DATE
GROUP BY op.nombre_producto
ORDER BY total_pedidos DESC

    """)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

@router.get("/graficas/top-clientes")
def top_clientes():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT cliente, COUNT(*) AS total_ordenes
FROM ordenes
WHERE DATE(fecha AT TIME ZONE 'America/Mexico_City') = CURRENT_DATE
GROUP BY cliente
ORDER BY total_ordenes DESC

    """)
    data = cursor.fetchall()
    cursor.close()
    db.close()
    return data

@router.get("/productos/menos-pedido")
def producto_menos_pedido():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT op.nombre_producto, SUM(op.cantidad) AS total_vendidos
FROM orden_productos op
JOIN ordenes o ON op.orden_id = o.id
WHERE DATE(o.fecha AT TIME ZONE 'America/Mexico_City') = CURRENT_DATE
GROUP BY op.nombre_producto
ORDER BY total_vendidos ASC
LIMIT 1

    """)
    data = cursor.fetchone()
    cursor.close()
    db.close()
    return data
