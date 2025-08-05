from fastapi import APIRouter, Form, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
from fastapi import Request
from uuid import uuid4
from datetime import datetime, timedelta
from utils.email_utils import enviar_correo_recuperacion
from database import get_db_connection
from config import BACKEND_URL, FRONTEND_URL
import os
from dotenv import load_dotenv

load_dotenv()


router = APIRouter()

PROFILE_UPLOAD_DIR = "assets/Perfiles"

@router.post("/login")
def login(correo: str = Form(...), contrasena: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM usuarios WHERE correo=%s AND contrasena=%s", (correo, contrasena))
    user = cursor.fetchone()
    cursor.close()
    db.close()

    if user:
        return {
            "success": True,
            "rol": user["rol"],
            "usuario_id": user["id"],
            "nombre": user["nombre"]
        }
    raise HTTPException(status_code=401, detail="Credenciales inválidas")

@router.post("/registro")
def register(
    nombre: str = Form(...),
    correo: str = Form(...),
    contrasena: str = Form(...),
    grado: str = Form(...),
    carrera: str = Form(...)
):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre, correo, contrasena, grado, carrera, rol) VALUES (%s, %s, %s, %s, %s, %s)",
            (nombre, correo, contrasena, grado, carrera, 'cliente')
        )
        db.commit()
        return {"success": True}
    except Exception as e:
        db.rollback()
        if hasattr(e, 'pgcode') and e.pgcode == '23505':
            raise HTTPException(status_code=400, detail="Correo ya registrado")
        raise HTTPException(status_code=500, detail="Error del servidor: " + str(e))
    finally:
        cursor.close()
        db.close()

@router.get("/usuarios/{usuario_id}")
def get_usuario(usuario_id: int):
    db = get_db_connection()
    cursor = db.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute("SELECT id, nombre, correo, foto FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if usuario["foto"]:
            usuario["foto_url"] = f"{BACKEND_URL}{usuario['foto']}"
        else:
            usuario["foto_url"] = None

        return usuario

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()

@router.put("/usuarios/{usuario_id}")
async def actualizar_usuario(usuario_id: int, 
                              nombre: str = Form(...),
                              correo: str = Form(...),
                              file: UploadFile = File(None)):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        foto_url = None
        if file:
            extension = file.filename.split('.')[-1].lower()
            if extension not in ["jpg", "jpeg", "png", "gif"]:
                raise HTTPException(status_code=400, detail="Formato de imagen no soportado")

            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_location = f"{PROFILE_UPLOAD_DIR}/{usuario_id}_{timestamp}.{extension}"

            with open(file_location, "wb") as f:
                f.write(file.file.read())

            foto_url = f"/assets/Perfiles/{os.path.basename(file_location)}"

        # Obtener correo anterior y rol
        cursor.execute("SELECT correo, rol FROM usuarios WHERE id = %s", (usuario_id,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        correo_anterior = user[0]
        rol_usuario = user[1]

        # Actualizar en usuarios
        if foto_url:
            cursor.execute("""
                UPDATE usuarios SET nombre = %s, correo = %s, foto = %s WHERE id = %s
            """, (nombre, correo, foto_url, usuario_id))
        else:
            cursor.execute("""
                UPDATE usuarios SET nombre = %s, correo = %s WHERE id = %s
            """, (nombre, correo, usuario_id))

        # Si el usuario es chef, actualizar también en empleados
        if rol_usuario == "chef":
            if foto_url:
                cursor.execute("""
                    UPDATE empleados SET nombre = %s, correo = %s, foto = %s WHERE correo = %s
                """, (nombre, correo, foto_url, correo_anterior))
            else:
                cursor.execute("""
                    UPDATE empleados SET nombre = %s, correo = %s WHERE correo = %s
                """, (nombre, correo, correo_anterior))

        db.commit()
        return {"success": True, "message": "Perfil y empleado actualizados correctamente si aplica."}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar perfil: {str(e)}")
    finally:
        cursor.close()
        db.close()

###rewcuperar contraseña
@router.post("/recuperar-contrasena")
def recuperar_contrasena(request: Request, correo: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        # Verifica si el correo existe
        cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Correo no registrado")

        # Genera token y fecha de expiración
        token = str(uuid4())
        expiracion = datetime.now() + timedelta(minutes=15)

        # Guarda token en la base de datos
        cursor.execute("""
            UPDATE usuarios SET token_recuperacion = %s, token_expira = %s WHERE correo = %s
        """, (token, expiracion, correo))
        db.commit()

        # Enlace
        
        #base_url = str(request.base_url).rstrip('/')
        #enlace = f"{base_url}/restablecer?token={token}"
        # En lugar de usar request.base_url...
# base_url = str(request.base_url).rstrip('/')
# enlace = f"{base_url}/restablecer?token={token}"

        # Haz esto:
        #frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")  # valor por defecto
        enlace = f"{FRONTEND_URL}/restablecer-contrasena?token={token}"

        enviar_correo_recuperacion(correo, enlace)

        return {"success": True, "message": "Correo enviado"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()


@router.post("/restablecer-contrasena")
def restablecer_contrasena(token: str = Form(...), nuevaContrasena: str = Form(...)):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        # Verificar token
        cursor.execute("""
            SELECT id, token_expira FROM usuarios WHERE token_recuperacion = %s
        """, (token,))
        usuario = cursor.fetchone()

        if not usuario:
            raise HTTPException(status_code=400, detail="Token inválido")

        if usuario[1] < datetime.now():
            raise HTTPException(status_code=400, detail="Token expirado")

        # Actualizar contraseña y limpiar token
        cursor.execute("""
            UPDATE usuarios
            SET contrasena = %s, token_recuperacion = NULL, token_expira = NULL
            WHERE id = %s
        """, (nuevaContrasena, usuario[0]))
        db.commit()

        return {"success": True, "message": "Contraseña actualizada"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()