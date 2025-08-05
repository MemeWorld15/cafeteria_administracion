# config.py
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", " https://6c097db88ac9.ngrok-free.app")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://cafeteria-administracion.vercel.app")
