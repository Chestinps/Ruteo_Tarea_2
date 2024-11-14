import os
import json
import psycopg2
from psycopg2.extras import execute_values
from geopy.distance import geodesic

# Conexión a la base de datos
conn = psycopg2.connect("dbname='ruteo_db' user='admin' password='admin123' host='localhost' port='5432'")
cur = conn.cursor()

# Obtener la ruta completa del archivo calles.geojson
script_dir = os.path.dirname(os.path.abspath(__file__))
geojson_path = os.path.join(script_dir, "calles.geojson")

# Cargar el archivo GeoJSON
with open(geojson_path) as f:
    data = json.load(f)

# Insertar edges en la tabla edges
edge_values = []
for i, feature in enumerate(data['features']):
    way_id = feature['properties']['way_id']
    coordinates = feature['geometry']['coordinates']
    
    # Crear edges entre cada par de nodos consecutivos
    for j in range(len(coordinates) - 1):
        start_coord = coordinates[j]
        end_coord = coordinates[j + 1]
        
        # Obtener los IDs de los nodos de inicio y destino
        cur.execute("SELECT id FROM nodes WHERE lat=%s AND lon=%s", (start_coord[1], start_coord[0]))
        source_id = cur.fetchone()
        
        cur.execute("SELECT id FROM nodes WHERE lat=%s AND lon=%s", (end_coord[1], end_coord[0]))
        target_id = cur.fetchone()
        
        # Verificar que ambos IDs se encontraron antes de continuar
        if source_id and target_id:
            source_id = source_id[0]
            target_id = target_id[0]
            
            # Calcular la distancia entre los puntos en metros
            cost = geodesic((start_coord[1], start_coord[0]), (end_coord[1], end_coord[0])).meters
            
            # Agregar los datos a la lista de edges
            edge_values.append((source_id, target_id, cost, cost, f'SRID=4326;LINESTRING({start_coord[0]} {start_coord[1]}, {end_coord[0]} {end_coord[1]})'))
    
    # Imprime el progreso cada 1000 features
    if i % 1000 == 0:
        print(f"Procesando feature {i + 1} de {len(data['features'])}")

# Inserción en bloque de todos los edges
print(f"Cantidad de edges a insertar: {len(edge_values)}")
execute_values(cur, """
    INSERT INTO edges (source, target, cost, reverse_cost, geom)
    VALUES %s
    """, [(source_id, target_id, cost, cost, geom) for source_id, target_id, cost, _, geom in edge_values])

# Confirmar los cambios en la base de datos
conn.commit()
cur.close()
conn.close()

print("Datos de edges insertados exitosamente.")