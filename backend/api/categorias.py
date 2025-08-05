from fastapi import APIRouter, Form, HTTPException
from database import get_db_connection
from psycopg2.extras import RealDictCursor

router = APIRouter()

@router.get("/categorias")
def listar_categorias():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()
    cursor.close()
    db.close()
    return categorias

@router.post("/categorias")
def crear_categoria(nombre: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO categorias (nombre) VALUES (%s)", (nombre,))
    db.commit()
    cursor.close()
    db.close()
    return {"success": True}

@router.put("/categorias/{categoria_id}")
def actualizar_categoria(categoria_id: int, nombre: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE categorias SET nombre = %s WHERE id = %s", (nombre, categoria_id))
    db.commit()
    cursor.close()
    db.close()
    return {"success": True}

@router.delete("/categorias/{categoria_id}")
def eliminar_categoria(categoria_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM categorias WHERE id = %s", (categoria_id,))
    db.commit()
    cursor.close()
    db.close()
    return {"success": True}
