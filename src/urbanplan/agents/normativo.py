# src/urbanplan/agents/normativo.py
from google_genai import types
# Nota: Ajusta las importaciones exactas según la versión del ADK de tu curso
from adk.tools import LlamaIndexRetrieval 
from adk.agents import Agent

def create_normativo_agent(index_path: str, provider: str = "gemini") -> Agent:
    """Crea el sub-agente experto en normativa urbanística."""
    
    # Conectamos la herramienta de recuperación al índice local
    retrieval_tool = LlamaIndexRetrieval(index_path=index_path)
    
    return Agent(
        name="agente_normativo",
        description="Experto en legislación urbanística, CTE y normativas del BOE.",
        model_provider=provider,
        system_instruction=(
            "Eres un arquitecto experto en normativa urbanística. "
            "Tu misión es consultar los documentos legales proporcionados y determinar "
            "la viabilidad legal de una obra. Si no encuentras la respuesta exacta "
            "en los documentos, DEBES indicar 'Información no encontrada' y no inventar datos."
        ),
        tools=[retrieval_tool]
    )