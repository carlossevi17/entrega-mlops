import os
import random
from dotenv import load_dotenv
from google.cloud import bigquery

load_dotenv()
project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "mlops-entrega")

client = bigquery.Client(project=project_id, location="EU")
dataset_id = f"{project_id}.agente_urbanistico"
table_id = f"{dataset_id}.licencias_historicas"

print("Borrando la tabla anterior y creando la nueva super-tabla...")
query_create = f"""
CREATE OR REPLACE TABLE `{table_id}` (
  tipo_obra STRING,
  municipio STRING,
  presupuesto_euros FLOAT64,
  tasa_licencia_euros FLOAT64,
  dias_tramitacion INT64,
  metros_cuadrados INT64,
  anio INT64
);
"""
client.query(query_create).result()

# Datos para generacion aleatoria
tipos = [
    "Obra mayor - Edificio residencial", "Obra mayor - Local comercial", 
    "Obra mayor - Hotel", "Obra mayor - Nave industrial", "Obra mayor - Hospital",
    "Obra menor - Reforma interior", "Obra menor - Ampliacion", 
    "Obra menor - Fachada", "Obra menor - Piscina", "Demolicion total"
]
municipios = [
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", 
    "Malaga", "Murcia", "Palma", "Las Palmas", "Bilbao"
]

print("Generando 100 registros realistas...")
insert_queries = []
for i in range(100):
    tipo = random.choice(tipos)
    municipio = random.choice(municipios)
    anio = random.randint(2018, 2024)
    
    if "mayor" in tipo:
        metros = random.randint(200, 5000)
        presupuesto = metros * random.uniform(800, 1500)
        dias = random.randint(90, 365)
    elif "menor" in tipo:
        metros = random.randint(10, 200)
        presupuesto = metros * random.uniform(200, 600)
        dias = random.randint(15, 90)
    else:
        metros = random.randint(100, 2000)
        presupuesto = metros * random.uniform(100, 300)
        dias = random.randint(30, 120)
        
    tasa = presupuesto * random.uniform(0.03, 0.05)  # 3% al 5% de ICIO+Tasas
    
    insert_queries.append(f"('{tipo}', '{municipio}', {presupuesto:.2f}, {tasa:.2f}, {dias}, {metros}, {anio})")

query_insert = f"INSERT INTO `{table_id}` VALUES\n" + ",\n".join(insert_queries) + ";"

print("Subiendo datos a BigQuery...")
client.query(query_insert).result()
print(f"[OK] ¡Insertados {len(insert_queries)} registros en {table_id}!")
