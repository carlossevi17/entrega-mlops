# src/urbanplan/mcp_server/server.py
from mcp.server.fastmcp import FastMCP
import os
from datetime import datetime

# Instanciamos el servidor MCP
mcp = FastMCP("UrbanPlan_Dossier_Server")

# Carpeta de salida para los informes generados
OUTPUT_DIR = os.path.abspath(os.path.join(os.getcwd(), "dossiers_generados"))
os.makedirs(OUTPUT_DIR, exist_ok=True)

@mcp.tool()
def generate_permit_dossier(
    project_title: str, 
    legal_viability_summary: str, 
    estimated_cost_euros: float, 
    estimated_days: int
) -> str:
    """
    Genera un dossier oficial de viabilidad urbanística estructurado en formato Markdown.
    Guarda el archivo en el sistema y devuelve la ruta de acceso.
    """
    
    # Formatear el nombre del archivo
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    safe_title = "".join(c if c.isalnum() else "_" for c in project_title).lower()
    filename = f"dossier_{safe_title}_{date_str}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Estructurar el contenido del informe
    content = f"""# Dossier de Proyecto: {project_title}
Generado por: UrbanPlan AI
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 1. Viabilidad Legal y Normativa (PGOU / CTE)
{legal_viability_summary}

## 2. Estimaciones de Ejecución (Histórico)
- **Coste Estimado de Licencias/Tasas:** {estimated_cost_euros} €
- **Plazo Medio de Resolución:** {estimated_days} días

---
*Nota: Este documento ha sido generado automáticamente como un resumen inicial de consultoría y debe ser revisado por un arquitecto colegiado.*
"""

    # Guardar en disco
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Dossier generado y guardado exitosamente en: {filepath}"
    except Exception as e:
        return f"Error crítico al guardar el dossier: {str(e)}"

if __name__ == "__main__":
    # Ejecuta el servidor usando el transporte estándar (stdio)
    print("Iniciando UrbanPlan MCP Server...", flush=True)
    mcp.run()