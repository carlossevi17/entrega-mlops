# src/urbanplan/agents/estimador.py
from google.adk.agents import Agent
from urbanplan.retrieval.bigquery import BigQueryEstimatorTool
from urbanplan.mcp_server.dossier_tool import generate_permit_dossier


def create_estimador_agent(bq_project_id: str, model: str = "gemini-2.5-flash") -> Agent:
    """Crea el sub-agente experto en presupuestos usando BigQuery."""

    bq_tool = BigQueryEstimatorTool(project_id=bq_project_id)

    def query_historical_data(query: str) -> str:
        """
        Ejecuta una consulta SQL de solo lectura (SELECT) contra la base de datos historica
        de licencias urbanisticas y devuelve los resultados en formato de texto.
        Solo acepta sentencias SELECT. Ejemplo de uso:
        SELECT * FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips` LIMIT 5
        """
        result = bq_tool.execute_read_only_query(query)
        if not result:
            return "La consulta no devolvio resultados."
        # Formateamos como texto legible
        output_lines = []
        for row in result[:20]:  # Mostramos max 20 filas al LLM
            output_lines.append(str(row))
        return f"Resultados ({len(result)} filas):\n" + "\n".join(output_lines)

    return Agent(
        name="agente_estimador",
        model=model,
        description="Experto en calcular estimaciones de plazos y presupuestos de obras basandose en datos historicos de BigQuery.",
        instruction=(
            "Eres un arquitecto tecnico experto en calculos de presupuestos y plazos de obra. "
            "Tienes acceso a una base de datos historica de licencias en BigQuery. "
            "La tabla principal es: `mlops-entrega.agente_urbanistico.licencias_historicas` "
            "con columnas: tipo_obra, municipio, presupuesto_euros, tasa_licencia_euros, dias_tramitacion, metros_cuadrados, anio. "
            "Cuando el usuario pregunte sobre costes o plazos, SIEMPRE consulta esa tabla con tu herramienta "
            "'query_historical_data' antes de responder. "
            "REGLA MUY IMPORTANTE: Si el usuario te pide informacion para una obra de un tamano o presupuesto exacto (ej. 250 metros), "
            "NUNCA filtres con `=` en SQL (ej. metros_cuadrados = 250). En su lugar, usa SIEMPRE rangos amplios con `BETWEEN` "
            "(ej. metros_cuadrados BETWEEN 200 AND 300) para asegurar que encuentras obras similares en la base de datos historica. "
            "Usa comodines (LIKE '%Local%') si no conoces el tipo_obra exacto. "
            "Ejemplo de consulta util: "
            "SELECT tipo_obra, AVG(tasa_licencia_euros) as tasa_media, AVG(dias_tramitacion) as dias_medios "
            "FROM `mlops-entrega.agente_urbanistico.licencias_historicas` "
            "WHERE metros_cuadrados BETWEEN 1000 AND 2000 AND municipio = 'Zaragoza' GROUP BY tipo_obra "
            "Si la consulta falla, proporciona una estimacion basada en el conocimiento del sector."
            "\n\nMUY IMPORTANTE: Tienes acceso a la herramienta 'generate_permit_dossier'. Si el usuario pide un informe o dossier, ÚSALA para guardar los datos."
        ),
        tools=[query_historical_data, generate_permit_dossier]
    )
