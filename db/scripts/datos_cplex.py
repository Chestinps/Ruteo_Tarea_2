import psycopg2
import json

# Conexión a la base de datos
def fetch_data():
    conn = psycopg2.connect(
        dbname="ruteo_db",
        user="admin",
        password="admin123",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Obtener nodos
    cursor.execute("""
        SELECT id, lat, lon, traffic_cost, has_traffic_bump, has_accidents 
        FROM nodes
    """)
    nodes = cursor.fetchall()

    # Obtener aristas
    cursor.execute("""
        SELECT id, source, target, cost, reverse_cost 
        FROM edges
    """)
    edges = cursor.fetchall()

    cursor.close()
    conn.close()

    return nodes, edges

# Guardar datos en formato GeoJSON o JSON
def save_data_to_geojson(nodes, edges, output_file="graph_data.json"):
    graph_data = {
        "nodes": [
            {
                "id": node[0],
                "lat": node[1],
                "lon": node[2],
                "traffic_cost": node[3],
                "has_traffic_bump": node[4],
                "has_accidents": node[5],
            }
            for node in nodes
        ],
        "edges": [
            {
                "id": edge[0],
                "source": edge[1],
                "target": edge[2],
                "cost": edge[3],
                "reverse_cost": edge[4],
            }
            for edge in edges
        ],
    }

    with open(output_file, "w") as f:
        json.dump(graph_data, f, indent=4)

# Ejecución
nodes, edges = fetch_data()
save_data_to_geojson(nodes, edges)
