# src/urbanplan/main.py
import os
from urbanplan.supervisor.agent import create_supervisor

# Cargar variables de entorno (simulando lo que haría dotenv o el propio ADK)
PROVIDER = os.getenv("MODEL_PROVIDER", "gemini")
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "tu-proyecto-gcp-12345")

# Construir rutas absolutas seguras
BASE_DIR = os.path.abspath(os.path.join(os.getcwd()))
INDEX_PATH = os.path.join(BASE_DIR, "data", "vector_store")

# Esta es la instancia que el ADK va a ejecutar
agent = create_supervisor(
    index_path=INDEX_PATH, 
    bq_project_id=PROJECT_ID, 
    provider=PROVIDER
)