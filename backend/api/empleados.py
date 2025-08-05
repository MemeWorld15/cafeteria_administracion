from fastapi import APIRouter, Form, HTTPException
from database import get_db_connection
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import Request

router = APIRouter()

@router.post("/empleados")
def crear_empleado(nombre: str = Form(...), correo: str = Form(...), ocupacion: str = Form(...), rendimiento: str = Form(...), contrasena: str = Form(...), creado_por: int = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    foto = f"https://i.pravatar.cc/150?img={abs(hash(correo)) % 70 + 1}"
    try:
        cursor.execute("""
            INSERT INTO empleados (nombre, correo, ocupacion, rendimiento, contrasena, foto, creado_por)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, correo, ocupacion, rendimiento, contrasena, foto, creado_por))

        if ocupacion.lower() == "chef":
            cursor.execute("""
                INSERT INTO usuarios (nombre, correo, contrasena, grado, carrera, rol)
                VALUES (%s, %s, %s, '-', '-', 'chef')
            """, (nombre, correo, contrasena))

        db.commit()
        return {"success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        db.close()

@router.get("/empleados")
def listar_empleados():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM empleados")
    empleados = cursor.fetchall()
    cursor.close()
    db.close()
    return empleados

@router.put("/empleados/{empleado_id}")
def actualizar_empleado(empleado_id: int, request: Request):
    db = get_db_connection()
    cursor = db.cursor()
    form = request.form()
    try:
        cursor.execute("""
            UPDATE empleados
            SET nombre = %s, correo = %s, ocupacion = %s, rendimiento = %s, contrasena = %s
            WHERE id = %s
        """, (
            form['nombre'], form['correo'], form['ocupacion'],
            form['rendimiento'], form['contrasena'], empleado_id
        ))
        db.commit()
        return {"success": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        db.close()

@router.delete("/empleados/{empleado_id}")
def eliminar_empleado(empleado_id: int):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT correo, ocupacion FROM empleados WHERE id = %s", (empleado_id,))
        empleado = cursor.fetchone()
        if not empleado:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")

        cursor.execute("DELETE FROM empleados WHERE id = %s", (empleado_id,))

        if empleado["ocupacion"].lower() == "chef":
            cursor.execute("DELETE FROM usuarios WHERE correo = %s AND rol = 'chef'", (empleado["correo"],))

        db.commit()
        return {"success": True, "message": "Empleado y usuario (si era chef) eliminados"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        db.close()
