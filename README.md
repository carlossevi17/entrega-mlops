# 🏙️ UrbanPlan AI

Un sistema de Inteligencia Artificial basado en Arquitectura Multi-Agente diseñado para asesorar sobre viabilidad legal, presupuestos y plazos de tramitación de licencias urbanísticas y de obra.

Este proyecto ha sido desarrollado utilizando **Google Agent Development Kit (ADK)** de Vertex AI, orquestando múltiples agentes potenciados por el modelo `gemini-2.5-flash`.

---

## 🚀 Arquitectura del Sistema

El proyecto implementa un patrón **Supervisor-Worker**, distribuyendo las tareas complejas entre especialistas:

1. **Supervisor (`supervisor_urbanplan`)**: 
   - Analiza la intención del usuario.
   - Enruta la petición al sub-agente experto correspondiente.
   - Es capaz de invocar la herramienta externa MCP para compilar y generar dossiers ejecutivos.
2. **Sub-Agente Normativo (`agente_normativo`)**: 
   - Arquitecto experto en el Código Técnico de la Edificación (CTE) y regulaciones del BOE. Responde a preguntas sobre viabilidad legal, alturas libres, normativas de incendios, etc., utilizando el conocimiento experto del LLM base.
3. **Sub-Agente Estimador (`agente_estimador`)**: 
   - Arquitecto Técnico especializado en costes y plazos.
   - **Grounding (BigQuery)**: No alucina precios. Genera y ejecuta dinámicamente **código SQL** contra una base de datos histórica alojada en Google Cloud Platform, garantizando que los cálculos (medias, sumas, análisis) sean matemáticamente exactos y basados en datos empíricos.

---

## 🛠️ Tecnologías y Prácticas MLOps

- **Framework de Agentes**: Google ADK (Agent Development Kit).
- **Modelos de Lenguaje**: `gemini-2.5-flash`.
- **Bases de Datos & Data Engineering**: Google BigQuery (`google-cloud-bigquery`). Script de automatización para creación y población masiva del dataset.
- **Tools / MCP**: Protocolos de herramientas nativas para operaciones I/O (escritura de archivos en `dossiers_generados/`).
- **Gestor de Entornos**: `uv` (Empaquetado rápido y determinista con soporte para `uv.lock`).
- **CI/CD Pipeline**: GitHub Actions automatizadas.
  - *Continuous Integration (CI)*: Checkout, instalación determinista de dependencias, y chequeo de sintaxis con `python -m py_compile` por cada push a `main`.
  - *Continuous Deployment (CD)*: Construcción de imagen Docker limpia y simulación de despliegue a **Google Cloud Run**.

---

## ⚙️ Configuración del Entorno (`.env` y Credenciales)

Para que el proyecto funcione en la máquina de otra persona (o del evaluador), es obligatorio configurar correctamente las credenciales de entorno y de nube.

### 1. Requisitos Previos
- Instalar Python 3.12+
- Instalar el gestor de paquetes ultrarrápido `uv`:
  ```bash
  pip install uv
  ```
- Tener instalada la línea de comandos de Google Cloud (`gcloud CLI`).

### 2. Autenticación en Google Cloud
Como el agente Estimador necesita hacer consultas reales a BigQuery, se debe tener una sesión activa con permisos en el proyecto de GCP. En la terminal, ejecuta:
```bash
gcloud auth application-default login
```
*Esto abrirá el navegador para iniciar sesión con la cuenta de Google que tenga acceso al proyecto.*

### 3. Archivo de Variables (`.env`)
En la raíz del proyecto, debes crear un archivo llamado `.env` y rellenarlo con los siguientes valores:

```env
# El identificador de tu proyecto en Google Cloud (donde estara alojado BigQuery)
GOOGLE_CLOUD_PROJECT=mi-id-de-proyecto-gcp

# Modelo de Gemini que empleara la arquitectura multi-agente
GEMINI_MODEL=gemini-2.5-flash
```

*(Importante para el evaluador: asegúrese de asignar a `GOOGLE_CLOUD_PROJECT` el ID de un proyecto de GCP sobre el cual tenga permisos de lectura/escritura en BigQuery).*

---

## 🚀 Despliegue en Local

### 1. Instalar Dependencias
Instala todas las dependencias exactamente como están definidas en la arquitectura:
```bash
uv sync --frozen
```

### 2. Poblar la Base de Datos (Solo si cambias de proyecto GCP)
La base de datos ya se encuentra desplegada y poblada con 100 registros en el proyecto original (`mlops-entrega`). 
**No hace falta ejecutar nada si mantienes ese proyecto y tienes acceso.**

Sin embargo, si clonas este repositorio y configuras en el `.env` un `GOOGLE_CLOUD_PROJECT` **nuevo o distinto**, debes inicializar la base de datos ejecutando el script de Data Engineering:
```bash
uv run python setup_bigquery.py
```
*(Esto se conectara a tu nuevo GCP, creara el dataset `agente_urbanistico` y la tabla, inyectando los 100 registros realistas para que el agente pueda funcionar).*

### 3. Arrancar el Agente ADK
Levanta el servidor local de agentes:
```bash
uv run adk web src
```
Accede en tu navegador a `http://localhost:8000` y chatea con `supervisor_urbanplan`.

---

## 💬 Casos de Uso y Prompts de Prueba

Para testear las capacidades del sistema en la interfaz de ADK, puedes probar estos Prompts:

1. **Test del Agente Normativo (Conocimiento Legal)**: 
   > *"¿Cuáles son los requisitos de altura libre mínima en viviendas según el CTE?"*

2. **Test del Agente Estimador (SQL Autónomo a BigQuery)**: 
   > *"Basándote en el histórico, ¿cuál es la tasa media de licencia y los días de tramitación para una obra mayor residencial en Madrid?"*

3. **Test de la Herramienta MCP (Escritura Automática de Ficheros)**: 
   > *"Calcula el presupuesto de una obra de local en Valencia de 200m2 y génerame un dossier en disco con los resultados."*

---

## 🐳 Despliegue en Producción (Docker)

El proyecto está preparado para *Continuous Deployment* e incluye un `Dockerfile` optimizado y libre de residuos locales.

Para compilar la imagen de producción:
```bash
docker build -t urbanplan-ai:latest .
```

Para correr el contenedor (asegurando el mapeo de credenciales de Google Cloud):
```bash
docker run -p 8080:8080 -e GOOGLE_APPLICATION_CREDENTIALS=/app/key.json -v /ruta/local/a/tu/key.json:/app/key.json urbanplan-ai:latest
```
