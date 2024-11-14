import os
import json
import psycopg2
from psycopg2.extras import execute_values

# Conexión a la base de datos
conn = psycopg2.connect("dbname='ruteo_db' user='admin' password='admin123' host='localhost' port='5432'")
cur = conn.cursor()

# Obtener la ruta completa del archivo calles.geojson
script_dir = os.path.dirname(os.path.abspath(__file__))
geojson_path = os.path.join(script_dir, "calles.geojson")

# Cargar el archivo GeoJSON
with open(geojson_path) as f:
    data = json.load(f)

# Insertar nodos únicos en la tabla nodes
unique_nodes = {}
for feature in data['features']:
    for coord in feature['geometry']['coordinates']:
        lon, lat = coord
        # Usar el par (lat, lon) como clave para asegurar unicidad
        unique_nodes[(lat, lon)] = (lat, lon)

# Verificar la cantidad de nodos únicos que se han encontrado
print(f"Cantidad de nodos únicos a insertar: {len(unique_nodes)}")

# Insertar nodos en lotes
node_values = [(f"SRID=4326;POINT({lon} {lat})", lat, lon) for lat, lon in unique_nodes.values()]
batch_size = 10000  # Tamaño del lote para la inserción

for i in range(0, len(node_values), batch_size):
    batch = node_values[i:i + batch_size]
    print(f"Inserting nodes batch {i // batch_size + 1} of {len(node_values) // batch_size + 1}")
    execute_values(cur, "INSERT INTO nodes (geom, lat, lon) VALUES %s ON CONFLICT DO NOTHING", batch)
    conn.commit()  # Confirmar cada lote para reducir el uso de memoria

# Confirmar los cambios en la base de datos
cur.close()
conn.close()

print("Datos de nodos insertados exitosamente.")