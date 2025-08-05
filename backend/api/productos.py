from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

from database import get_db_connection

router = APIRouter()

UPLOAD_DIR = "assets/food"

@router.get("/menu")
def obtener_menu():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)

    # Obtener todas las categorías
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    menu = {}
    for cat in categorias:
        cursor.execute("SELECT * FROM productos WHERE categoria_id = %s", (cat['id'],))
        productos = cursor.fetchall()
        menu[cat['nombre']] = productos

    cursor.close()
    db.close()
    return menu

@router.post("/productos/{producto_id}/imagen")
def subir_imagen(producto_id: int, file: UploadFile = File(...)):
    extension = file.filename.split('.')[-1].lower()
    if extension not in ["jpg", "jpeg", "png", "gif"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no soportado")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_location = f"{UPLOAD_DIR}/{producto_id}_{timestamp}.{extension}"

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    image_url = f"/assets/food/{os.path.basename(file_location)}"

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        UPDATE productos
        SET imagen_url = %s
        WHERE id = %s
    """, (image_url, producto_id))
    db.commit()
    cursor.close()
    db.close()

    return JSONResponse(content={"success": True, "image_url": image_url})

@router.post("/productos")
def crear_producto(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    categoria_id: int = Form(...),
    file: UploadFile = File(None)
):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO productos (nombre, descripcion, precio, categoria_id)
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (nombre, descripcion, precio, categoria_id))
    producto_id = cursor.fetchone()[0]
    db.commit()

    image_url = None
    if file:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        extension = file.filename.split('.')[-1].lower()
        file_location = f"{UPLOAD_DIR}/{producto_id}_{timestamp}.{extension}"

        with open(file_location, "wb") as f:
            f.write(file.file.read())

        image_url = f"/assets/food/{os.path.basename(file_location)}"
        cursor.execute("""
            UPDATE productos
            SET imagen_url = %s
            WHERE id = %s
        """, (image_url, producto_id))
        db.commit()

    cursor.close()
    db.close()

    return {"success": True, "producto_id": producto_id, "image_url": image_url}

@router.get("/productos")
def listar_productos():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    cursor.close()
    db.close()
    return productos

@router.put("/productos/{producto_id}")
def editar_producto(
    producto_id: int,
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    categoria_id: int = Form(...),
    file: UploadFile = File(None)
):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT imagen_url FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        db.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if file:
        imagen_actual = producto.get("imagen_url")
        if imagen_actual:
            ruta_imagen = f".{imagen_actual}"
            if os.path.exists(ruta_imagen):
                os.remove(ruta_imagen)

        extension = file.filename.split('.')[-1].lower()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_location = f"{UPLOAD_DIR}/{producto_id}_{timestamp}.{extension}"

        with open(file_location, "wb") as f:
            f.write(file.file.read())

        image_url = f"/assets/food/{os.path.basename(file_location)}"

        cursor.execute("""
            UPDATE productos
            SET imagen_url = %s
            WHERE id = %s
        """, (image_url, producto_id))

    cursor.execute("""
        UPDATE productos
        SET nombre=%s, descripcion=%s, precio=%s, categoria_id=%s
        WHERE id=%s
    """, (nombre, descripcion, precio, categoria_id, producto_id))

    db.commit()
    cursor.close()
    db.close()
    return {"success": True}

@router.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)

    cursor.execute("SELECT imagen_url FROM productos WHERE id = %s", (producto_id,))
    producto = cursor.fetchone()

    if not producto:
        cursor.close()
        db.close()
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    imagen_actual = producto.get("imagen_url")
    if imagen_actual:
        ruta_imagen = f".{imagen_actual}"
        if os.path.exists(ruta_imagen):
            os.remove(ruta_imagen)

    cursor.execute("DELETE FROM productos WHERE id = %s", (producto_id,))
    db.commit()
    cursor.close()
    db.close()
    return {"success": True}

@router.put("/productos/{producto_id}/toggle-disponible")
def toggle_disponibilidad(producto_id: int):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE productos SET disponible = NOT disponible WHERE id = %s", (producto_id,))
    db.commit()
    cursor.close()
    db.close()
    return {"success": True}
