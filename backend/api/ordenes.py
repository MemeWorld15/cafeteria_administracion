from fastapi import APIRouter, HTTPException
from models import OrdenEntrada
from database import get_db_connection
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
import pytz

router = APIRouter()

# Asegúrate que la tabla tenga estas columnas:
# ALTER TABLE ordenes
#   ADD COLUMN cancelada BOOLEAN DEFAULT FALSE,
#   ADD COLUMN motivo_cancelacion TEXT DEFAULT '';

@router.post("/ordenar")
def crear_orden(data: OrdenEntrada):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO ordenes (cliente, nota, usuario_id, entregado, turno)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (data.cliente, data.nota, data.usuario_id, False, data.turno))
        orden_id = cursor.fetchone()[0]

        for prod in data.productos:
            cursor.execute("""
                INSERT INTO orden_productos (orden_id, nombre_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s)
            """, (orden_id, prod.nombre, prod.cantidad, prod.precio))

        db.commit()
        return {"success": True, "orden_id": orden_id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()

@router.get("/ordenes")
def listar_ordenes():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)

    zona_mexico = pytz.timezone("America/Mexico_City")
    hoy = datetime.now(zona_mexico).date()

    cursor.execute("""
        SELECT * FROM ordenes
        WHERE DATE(fecha AT TIME ZONE 'America/Mexico_City') = %s
        ORDER BY id DESC
    """, (hoy,))
    ordenes = cursor.fetchall()

    for orden in ordenes:
        cursor.execute("SELECT * FROM orden_productos WHERE orden_id = %s", (orden["id"],))
        orden["productos"] = cursor.fetchall()
        orden["hora"] = orden["fecha"].strftime("%I:%M %p")
        orden["fecha_mostrada"] = orden["fecha"].strftime("%d-%m-%Y")
        orden["motivo_cancelacion"] = orden.get("motivo_cancelacion", "")

    cursor.close()
    db.close()
    return ordenes

@router.patch("/ordenes/{orden_id}/cancelar-por-cliente")
def cancelar_orden_por_cliente(orden_id: int):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT fecha, entregado, cancelada FROM ordenes WHERE id = %s", (orden_id,))
    orden = cursor.fetchone()

    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    if orden["entregado"]:
        raise HTTPException(status_code=400, detail="La orden ya fue entregada")
    if orden["cancelada"]:
        raise HTTPException(status_code=400, detail="La orden ya está cancelada")

    zona_mexico = pytz.timezone("America/Mexico_City")
    ahora = datetime.now(zona_mexico)
    fecha_orden = orden["fecha"].replace(tzinfo=zona_mexico)

    if ahora - fecha_orden > timedelta(minutes=2):
        raise HTTPException(status_code=403, detail="La orden ya no se puede cancelar")

    motivo = "Cancelado por el cliente."
    cursor.execute(
        "UPDATE ordenes SET cancelada = TRUE, motivo_cancelacion = %s WHERE id = %s",
        (motivo, orden_id)
    )
    db.commit()
    cursor.close()
    db.close()
    return {"success": True, "message": motivo}

@router.get("/ordenes/cliente/{usuario_id}")
def obtener_ordenes_cliente(usuario_id: int):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM ordenes WHERE usuario_id = %s ORDER BY id DESC", (usuario_id,))
    ordenes = cursor.fetchall()

    for orden in ordenes:
        cursor.execute("SELECT * FROM orden_productos WHERE orden_id = %s", (orden["id"],))
        orden["productos"] = cursor.fetchall()
        orden["hora"] = orden["fecha"].strftime("%I:%M %p")
        orden["fecha_mostrada"] = orden["fecha"].strftime("%d-%m-%Y")
        orden["motivo_cancelacion"] = orden.get("motivo_cancelacion", "")

    cursor.close()
    db.close()
    return ordenes

@router.put("/ordenes/{orden_id}/entregado")
def marcar_entregado(orden_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("UPDATE ordenes SET entregado = TRUE WHERE id = %s", (orden_id,))
        db.commit()
        return {"success": True}
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="No se pudo actualizar el estado de la orden")
    finally:
        cursor.close()
        db.close()

@router.patch("/ordenes/{orden_id}/cancelar-por-cocina")
def cancelar_orden_cocina_con_mensaje(orden_id: int):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("SELECT entregado, cancelada FROM ordenes WHERE id = %s", (orden_id,))
        orden = cursor.fetchone()

        if not orden:
            raise HTTPException(status_code=404, detail="Orden no encontrada")

        if orden["entregado"]:
            raise HTTPException(status_code=400, detail="La orden ya fue entregada")

        if orden["cancelada"]:
            raise HTTPException(status_code=400, detail="La orden ya está cancelada")

        mensaje_cancelacion = "Lo sentimos, este pedido ha sido cancelado por la cocina."
        cursor.execute(
            "UPDATE ordenes SET cancelada = TRUE, motivo_cancelacion = %s WHERE id = %s",
            (mensaje_cancelacion, orden_id)
        )
        db.commit()

        return {"success": True, "message": mensaje_cancelacion}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        cursor.close()
        db.close()
