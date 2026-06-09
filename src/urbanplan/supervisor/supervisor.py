# src/urbanplan/supervisor/supervisor.py
import os
from google.adk.agents import Agent
from urbanplan.agents.normativo import create_normativo_agent
from urbanplan.agents.estimador import create_estimador_agent
from urbanplan.mcp_server.dossier_tool import generate_permit_dossier

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def create_supervisor(bq_project_id: str, model: str = "gemini-2.5-flash") -> Agent:
    """Orquesta el sistema delegando en sub-agentes especializados."""

    # 1. Instanciar sub-agentes
    normativo = create_normativo_agent(model)
    estimador = create_estimador_agent(bq_project_id, model)

    # 2. Crear el Supervisor con sub_agents y la herramienta MCP directa
    return Agent(
        name="supervisor_urbanplan",
        model=model,
        description="Director de consultoria urbanistica UrbanPlan AI.",
        instruction=(
            "Eres el director de una consultora urbanistica llamada UrbanPlan AI. "
            "Tienes a tu disposicion un equipo especializado:\n\n"
            "- 'agente_normativo': Experto en legislacion urbanistica, BOE y CTE. "
            "Delégale preguntas sobre viabilidad legal, normativa de alturas, usos del suelo, accesibilidad, etc.\n"
            "- 'agente_estimador': Experto en presupuestos y plazos historicos de obras. "
            "Delégale preguntas sobre costes estimados, tasas de licencia o tiempos de tramitacion.\n"
            "- 'generate_permit_dossier': Herramienta que genera un dossier oficial en Markdown. "
            "Usala cuando el usuario pida el INFORME FINAL o DOSSIER del proyecto.\n\n"
            "Flujo para un dossier completo:\n"
            "1. Transfiere al agente_normativo para obtener la viabilidad legal.\n"
            "2. Transfiere al agente_estimador para obtener costes y plazos.\n"
            "3. Con ambas respuestas, llama a generate_permit_dossier para generar el archivo.\n"
            "4. Informa al usuario de la ruta donde se ha guardado el documento.\n\n"
            "Si el usuario hace una pregunta general de urbanismo, delegala al agente_normativo. "
            "Si pregunta sobre presupuesto o plazos, delegala al agente_estimador."
        ),
        tools=[generate_permit_dossier],
        sub_agents=[normativo, estimador],
    )