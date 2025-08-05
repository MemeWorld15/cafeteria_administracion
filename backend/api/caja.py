from fastapi import APIRouter, HTTPException, Request
from database import get_db_connection
from psycopg2.extras import RealDictCursor
import json

router = APIRouter()

@router.get("/caja")
def listar_cortes_caja():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT * FROM caja ORDER BY fecha DESC, id DESC")
        cortes = cursor.fetchall()
        return cortes
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener cortes de caja: " + str(e))
    finally:
        cursor.close()
        db.close()

@router.post("/caja")
async def guardar_corte_caja(request: Request):
    data = await request.json()
    fecha = data.get("fecha")
    turno = data.get("turno")
    total_ventas = data.get("totalVentas")
    gastos = data.get("gastos")
    total_gastos = data.get("totalGastos")
    monto_caja = data.get("montoCaja")
    resultado = data.get("resultado")

    if not fecha or not turno or total_ventas is None:
        raise HTTPException(status_code=400, detail="Datos incompletos para guardar corte")

    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO caja (fecha, turno, total_ventas, gastos, total_gastos, monto_caja, resultado)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            fecha,
            turno,
            total_ventas,
            json.dumps(gastos),
            total_gastos,
            monto_caja,
            resultado
        ))
        db.commit()
        return {"success": True, "message": "Corte de caja guardado correctamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error al guardar el corte: " + str(e))
    finally:
        cursor.close()
        db.close()
