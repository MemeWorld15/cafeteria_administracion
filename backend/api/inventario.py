from fastapi import APIRouter, HTTPException, Form
from database import get_db_connection
from psycopg2.extras import RealDictCursor
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
from datetime import datetime
from fastapi import Query

router = APIRouter()

UNIDADES_VALIDAS = ["kg", "g", "l", "ml", "piezas"]

# 📝 Función auxiliar para registrar movimientos
def registrar_movimiento(insumo_id: int, tipo: str, cantidad: float, unidad: str):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO movimientos_inventario (insumo_id, tipo_movimiento, cantidad, unidad) VALUES (%s, %s, %s, %s)",
        (insumo_id, tipo, cantidad, unidad)
    )
    db.commit()
    cursor.close()
    db.close()

@router.get("/inventario")
def listar_inventario():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM inventario")
    items = cursor.fetchall()
    cursor.close()
    db.close()
    return items

@router.post("/inventario")
def agregar_insumo(nombre: str = Form(...), cantidad: float = Form(...), unidad: str = Form(...)):
    if cantidad < 0:
        raise HTTPException(status_code=400, detail="Cantidad inválida")
    if unidad not in UNIDADES_VALIDAS:
        raise HTTPException(status_code=400, detail="Unidad no permitida")

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO inventario (nombre, cantidad, unidad) VALUES (%s, %s, %s) RETURNING id", (nombre, cantidad, unidad))
    insumo_id = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    db.close()

    registrar_movimiento(insumo_id, "agregado", cantidad, unidad)

    return {"success": True}

@router.put("/inventario/{id}")
def actualizar_cantidad(id: int, cantidad: float = Form(...)):
    if cantidad < 0:
        raise HTTPException(status_code=400, detail="Cantidad inválida")
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE inventario SET cantidad = %s WHERE id = %s", (cantidad, id))
    db.commit()
    cursor.close()
    db.close()
    return {"success": True}

@router.delete("/inventario/{id}")
def eliminar_insumo(id: int):
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute("SELECT cantidad, unidad FROM inventario WHERE id = %s", (id,))
    item = cursor.fetchone()

    if item:
        registrar_movimiento(id, "eliminacion", item[0], item[1])

    cursor.execute("DELETE FROM inventario WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return {"success": True}

@router.put("/inventario/{id}/editar")
def editar_insumo(id: int, nombre: str = Form(...), unidad: str = Form(...)):
    if unidad not in UNIDADES_VALIDAS:
        raise HTTPException(status_code=400, detail="Unidad no permitida")

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("UPDATE inventario SET nombre = %s, unidad = %s WHERE id = %s", (nombre, unidad, id))
    db.commit()
    cursor.close()
    db.close()

    registrar_movimiento(id, "edicion", 0, unidad)
    return {"success": True}

@router.post("/inventario/{id}/consumir")
def consumir_insumo(id: int, cantidad_usada: float = Form(...), unidad: str = Form(...)):
    if cantidad_usada <= 0:
        raise HTTPException(status_code=400, detail="Cantidad inválida")

    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT cantidad, unidad FROM inventario WHERE id = %s", (id,))
    insumo = cursor.fetchone()

    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")

    def convertir(valor, de, a):
        conversiones = {
            "kg": {"g": lambda v: v * 1000},
            "g": {"kg": lambda v: v / 1000},
            "l": {"ml": lambda v: v * 1000},
            "ml": {"l": lambda v: v / 1000}
        }
        return valor if de == a else conversiones.get(de, {}).get(a, lambda v: None)(valor)

    cantidad_convertida = convertir(cantidad_usada, unidad, insumo["unidad"])
    if cantidad_convertida is None:
        raise HTTPException(status_code=400, detail="Unidades incompatibles")

    nueva_cantidad = insumo["cantidad"] - cantidad_convertida
    if nueva_cantidad < 0:
        raise HTTPException(status_code=400, detail="Cantidad insuficiente")

    cursor.execute("UPDATE inventario SET cantidad = %s WHERE id = %s", (nueva_cantidad, id))
    db.commit()
    cursor.close()
    db.close()

    registrar_movimiento(id, "consumo", cantidad_usada, unidad)
    return {"success": True}

@router.post("/inventario/{id}/reabastecer")
def reabastecer_insumo(id: int, cantidad_agregada: float = Form(...), unidad: str = Form(...)):
    if cantidad_agregada <= 0:
        raise HTTPException(status_code=400, detail="Cantidad inválida")

    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT cantidad, unidad FROM inventario WHERE id = %s", (id,))
    insumo = cursor.fetchone()

    if not insumo:
        raise HTTPException(status_code=404, detail="Insumo no encontrado")

    def convertir(valor, de, a):
        conversiones = {
            "kg": {"g": lambda v: v * 1000},
            "g": {"kg": lambda v: v / 1000},
            "l": {"ml": lambda v: v * 1000},
            "ml": {"l": lambda v: v / 1000}
        }
        return valor if de == a else conversiones.get(de, {}).get(a, lambda v: None)(valor)

    cantidad_convertida = convertir(cantidad_agregada, unidad, insumo["unidad"])
    if cantidad_convertida is None:
        raise HTTPException(status_code=400, detail="Unidades incompatibles")

    nueva_cantidad = insumo["cantidad"] + cantidad_convertida
    cursor.execute("UPDATE inventario SET cantidad = %s WHERE id = %s", (nueva_cantidad, id))
    db.commit()
    cursor.close()
    db.close()

    registrar_movimiento(id, "reabastecimiento", cantidad_agregada, unidad)
    return {"success": True}

@router.get("/inventario/historial")
def historial_inventario(
    nombre: str = Query(default="", alias="nombre"),
    tipo: str = Query(default="", alias="tipo_movimiento")
):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    
    query = """
    SELECT m.id, m.insumo_id, i.nombre AS insumo, m.tipo_movimiento, m.cantidad, m.unidad, m.fecha
    FROM movimientos_inventario m
    JOIN inventario i ON i.id = m.insumo_id
    """
    filtros = []
    params = []

    if nombre:
        filtros.append("LOWER(i.nombre) LIKE LOWER(%s)")
        params.append(f"%{nombre}%")
    if tipo:
        filtros.append("m.tipo_movimiento = %s")
        params.append(tipo)

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    query += " ORDER BY m.fecha DESC"

    cursor.execute(query, tuple(params))
    historial = cursor.fetchall()
    cursor.close()
    db.close()
    return historial

@router.get("/inventario/pdf")
def generar_pdf_inventario():
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT nombre, cantidad, unidad FROM inventario ORDER BY nombre")
    items = cursor.fetchall()
    cursor.close()
    db.close()

    filename = f"Inventario_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = f"/tmp/{filename}" if os.name != "nt" else filename

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#2c3e50"))
    c.drawString(40, height - 50, "📦 Reporte de Inventario - Cafetería")

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(40, height - 70, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    logo_path = os.path.join("static", "Logos.png")
    abs_logo_path = os.path.abspath(logo_path)

    try:
        if os.path.exists(abs_logo_path):
            logo_width = 100
            logo_height = 100
            logo_x = width - logo_width - 50
            logo_y = height - 120
            c.drawImage(abs_logo_path, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print("⚠️ Error al cargar imagen:", e)

    data = [["Nombre", "Cantidad", "Unidad"]]
    for item in items:
        data.append([item["nombre"], f"{item['cantidad']:.2f}", item["unidad"]])

    table = Table(data, colWidths=[250, 100, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#3498db")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, 40, height - 400)
    c.setFont("Helvetica-Oblique", 8)
    c.drawRightString(width - 40, 30, f"Página 1")
    c.save()

    return FileResponse(filepath, media_type='application/pdf', filename=filename)

@router.post("/inventario/{id}/deshacer_ultimo")
def deshacer_ultimo_movimiento(id: int):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT * FROM movimientos_inventario
        WHERE insumo_id = %s
        ORDER BY fecha DESC
        LIMIT 1
    """, (id,))
    mov = cursor.fetchone()
    if not mov:
        raise HTTPException(404, detail="Sin movimientos")

    if mov["tipo_movimiento"] == "consumo":
        operacion = "+"
    elif mov["tipo_movimiento"] == "reabastecimiento":
        operacion = "-"
    else:
        raise HTTPException(400, detail="Este tipo no se puede deshacer")

    cursor.execute("SELECT cantidad FROM inventario WHERE id = %s", (id,))
    actual = cursor.fetchone()["cantidad"]

    nueva_cantidad = actual + mov["cantidad"] if operacion == "+" else actual - mov["cantidad"]
    if nueva_cantidad < 0:
        raise HTTPException(400, detail="No se puede revertir: resultado negativo")

    cursor.execute("UPDATE inventario SET cantidad = %s WHERE id = %s", (nueva_cantidad, id))
    registrar_movimiento(id, f"revertir_{mov['tipo_movimiento']}", mov["cantidad"], mov["unidad"])

    db.commit()
    cursor.close()
    db.close()
    return {"success": True}
