# src/urbanplan/supervisor/agent.py
import os
from adk.agents import Agent
from adk.tools import AgentTool, McpTool
from urbanplan.agents.normativo import create_normativo_agent
from urbanplan.agents.estimador import create_estimador_agent

def create_supervisor(index_path: str, bq_project_id: str, provider: str = "gemini") -> Agent:
    """Orquesta el sistema delegando en sub-agentes y herramientas MCP."""
    
    # 1. Instanciar los sub-agentes
    normativo = create_normativo_agent(index_path, provider)
    estimador = create_estimador_agent(bq_project_id, provider)
    
    # Envolverlos como herramientas
    tool_normativo = AgentTool(agent=normativo)
    tool_estimador = AgentTool(agent=estimador)
    
    # 2. Conectar el Servidor MCP (Infraestructura MCP)
    # Se conecta mediante la entrada estándar (stdio) lanzando el script en un subproceso
    mcp_server_path = os.path.abspath(os.path.join(os.getcwd(), "src", "urbanplan", "mcp_server", "server.py"))
    mcp_dossier_tool = McpTool(
        command="uv",
        args=["run", "python", mcp_server_path]
    )
    
    # 3. Crear el Supervisor
    return Agent(
        name="supervisor_urbanplan",
        model_provider=provider,
        system_instruction=(
            "Eres el director de una consultora urbanística. Trabajas orquestando a tu equipo:\n"
            "1. Usa 'agente_normativo' para resolver dudas de viabilidad legal y normativa.\n"
            "2. Usa 'agente_estimador' para calcular plazos y presupuestos históricos.\n"
            "3. Cuando el usuario te pida el INFORME o DOSSIER FINAL, debes asegurarte de tener "
            "tanto la viabilidad legal como las estimaciones. Una vez tengas esa información, "
            "usa la herramienta MCP 'generate_permit_dossier' para generar el archivo físico. "
            "Informa siempre al usuario de la ruta donde se ha guardado su documento."
        ),
        tools=[tool_normativo, tool_estimador, mcp_dossier_tool]
    )