# src/urbanplan/mcp_server/dossier_tool.py
"""
Herramienta MCP de generación de dossier urbanístico.
Expuesta al supervisor como función Python para máxima compatibilidad.
El servidor MCP completo (server.py) está disponible para modo stdio.
"""
import os
from datetime import datetime


def generate_permit_dossier(
    project_title: str,
    legal_viability_summary: str,
    estimated_cost_euros: float,
    estimated_days: int
) -> str:
    """
    Genera un dossier oficial de viabilidad urbanística en formato Markdown y lo guarda en disco.
    Devuelve la ruta completa del archivo generado.

    Args:
        project_title: Título del proyecto de obra o urbanístico.
        legal_viability_summary: Resumen de la viabilidad legal y normativa.
        estimated_cost_euros: Coste estimado de tasas/licencias en euros.
        estimated_days: Plazo medio estimado de resolución en días.
    """
    output_dir = os.path.abspath(os.path.join(os.getcwd(), "dossiers_generados"))
    os.makedirs(output_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    safe_title = "".join(c if c.isalnum() else "_" for c in project_title).lower()
    filename = f"dossier_{safe_title}_{date_str}.md"
    filepath = os.path.join(output_dir, filename)

    content = f"""# Dossier de Proyecto: {project_title}
**Generado por:** UrbanPlan AI  
**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## 1. Viabilidad Legal y Normativa (PGOU / CTE / BOE)

{legal_viability_summary}

---

## 2. Estimaciones de Ejecución (Fuente: Histórico Municipal)

| Concepto | Valor |
|---|---|
| **Coste Estimado de Licencias/Tasas** | {estimated_cost_euros:,.2f} € |
| **Plazo Medio de Resolución** | {estimated_days} días hábiles |

---

*⚠️ Nota: Este documento ha sido generado automáticamente por UrbanPlan AI como resumen inicial de consultoría. Debe ser revisado y validado por un arquitecto colegiado antes de su presentación oficial.*
"""

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ Dossier generado y guardado en: {filepath}"
    except Exception as e:
        return f"❌ Error al guardar el dossier: {str(e)}"
