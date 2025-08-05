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
    allow_origins=["https://cafeteria-administracion.vercel.app/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/assets/food", StaticFiles(directory="assets/food"), name="assets-food")
Path("assets/food").mkdir(parents=True, exist_ok=True)

app.mount("/assets/Perfiles", StaticFiles(directory="assets/Perfiles"), name="assets-perfiles")
Path("assets/Perfiles").mkdir(parents=True, exist_ok=True)

# Crear la carpeta static si no existe
if not os.path.exists("static"):
    os.makedirs("static")

# Montar la carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

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
