# src/urbanplan/agents/normativo.py
from google.adk.agents import Agent

def create_normativo_agent(model: str = "gemini-2.5-flash") -> Agent:
    """Crea el sub-agente experto en normativa urbanistica general."""

    return Agent(
        name="agente_normativo",
        model=model,
        description="Experto en legislacion urbanistica, CTE y normativas del BOE. Usalo para determinar la viabilidad legal de obras y proyectos.",
        instruction=(
            "Eres un arquitecto experto en normativa urbanistica espanola. "
            "Tu mision es asesorar sobre la viabilidad legal de una obra o proyecto "
            "basandote en tu profundo conocimiento del Codigo Tecnico de la Edificacion (CTE) y las normativas habituales. "
            "Responde de forma profesional, clara y concisa."
        )
    )