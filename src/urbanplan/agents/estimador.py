# src/urbanplan/agents/estimador.py
from google.adk.agents import Agent
from urbanplan.retrieval.bigquery import BigQueryEstimatorTool


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
            "Ejemplo de consulta util: "
            "SELECT tipo_obra, AVG(tasa_licencia_euros) as tasa_media, AVG(dias_tramitacion) as dias_medios "
            "FROM `mlops-entrega.agente_urbanistico.licencias_historicas` "
            "WHERE presupuesto_euros BETWEEN 300000 AND 500000 GROUP BY tipo_obra "
            "Si la consulta falla, proporciona una estimacion basada en el conocimiento del sector espanol."
        ),
        tools=[query_historical_data]
    )
