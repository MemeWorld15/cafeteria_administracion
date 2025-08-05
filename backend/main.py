from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import uvicorn


# Crear instancia FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://cafeteria-administracion.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta ABSOLUTA al directorio (funciona en cualquier entorno)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
assets_path = os.path.join(BASE_DIR, "backend", "assets", "food")  # Ajusta según tu estructura

# Verifica si la carpeta existe (opcional, para debug)
if not os.path.exists(assets_path):
    raise RuntimeError(f"No se encontró: {assets_path}")

app.mount("/assets/food", StaticFiles(directory=assets_path), name="food")

# Incluir routers de la carpeta api
from api import (
    usuarios,
    productos,
    categorias,
    ordenes,
    empleados,
    inventario,
    graficas,
    caja
)

app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(ordenes.router)
app.include_router(empleados.router)
app.include_router(inventario.router)
app.include_router(graficas.router)
app.include_router(caja.router)

# Ruta raíz
@app.get("/")
def root():
    return {"message": "¡La API está funcionando correctamente!"}

# Ejecutar con uvicorn
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
