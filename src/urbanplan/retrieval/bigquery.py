# src/urbanplan/retrieval/bigquery.py
from google.cloud import bigquery
import re

class BigQueryEstimatorTool:
    def __init__(self, project_id: str):
        # Aseguramos que la región sea EU, que es donde se creó el dataset
        self.client = bigquery.Client(project=project_id, location="EU")
        
        # Límite obligatorio de bytes facturables para evitar costes descontrolados
        self.job_config = bigquery.QueryJobConfig(
            maximum_bytes_billed=100000000  # 100 MB de límite por consulta
        )

    def execute_read_only_query(self, query: str) -> list[dict]:
        """Ejecuta una consulta SQL asegurando que es de solo lectura y tiene un límite."""
        
        # 1. Validación de seguridad: Solo SELECT permitidos
        if not re.match(r"^\s*SELECT", query, re.IGNORECASE):
            raise ValueError("Error de seguridad: Solo se permiten sentencias SELECT.")
        
        # Bloquear comandos destructivos o de modificación
        forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "TRUNCATE", "ALTER"]
        if any(keyword in query.upper() for keyword in forbidden_keywords):
            raise ValueError("Error de seguridad: Sentencia no permitida detectada.")

        # 2. Forzar un límite de filas (Ej. LIMIT 1000)
        if "LIMIT" not in query.upper():
            query = f"{query}\nLIMIT 1000"

        try:
            query_job = self.client.query(query, job_config=self.job_config)
            results = query_job.result()
            return [dict(row) for row in results]
        except Exception as e:
            return [{"error": str(e)}]