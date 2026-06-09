# src/urbanplan/agent.py
import os
from dotenv import load_dotenv
from urbanplan.supervisor.supervisor import create_supervisor

# Cargar .env automaticamente
load_dotenv()

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "mlops-entrega")

# Construir rutas absolutas
BASE_DIR = os.path.abspath(os.getcwd())

# ADK busca 'root_agent' — nombre obligatorio
root_agent = create_supervisor(
    bq_project_id=PROJECT_ID,
    model=MODEL,
)