from flask import Flask, render_template, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import json

app = Flask(__name__)

# Configuración de conexión a la base de datos
DB_CONFIG = {
    'dbname': 'ruteo_db',
    'user': 'admin',
    'password': 'admin123',
    'host': 'localhost',
    'port': '5433'
}

# Ruta para servir la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para cargar las estaciones de bomberos desde la base de datos
@app.route('/data/fire_stations')
def fire_stations():
    try:
        # Conectar a la base de datos y obtener las estaciones de bomberos
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Consulta para obtener todas las estaciones de bomberos
        cur.execute("""
            SELECT id, lat, lon, tags
            FROM estaciones_bomberos;
        """)
        stations = cur.fetchall()

        # Convertir a formato GeoJSON
        geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [station['lon'], station['lat']]
                    },
                    "properties": {
                        "id": station['id'],
                        "tags": station['tags']
                    }
                }
                for station in stations
            ]
        }

        cur.close()
        conn.close()

        print("Fire stations data loaded successfully.")
        return jsonify(geojson)

    except Exception as e:
        print(f"Error loading fire stations from database: {e}")
        return jsonify({'error': 'Unable to load fire stations data'}), 500

# Ruta para recibir las coordenadas de emergencia y calcular la ruta óptima
@app.route('/set_emergency', methods=['POST'])
def set_emergency():
    data = request.get_json()
    emergency_lat = data.get('latitude')
    emergency_lng = data.get('longitude')

    try:
        # Conectar a la base de datos
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Encontrar la estación de bomberos más cercana al punto de emergencia
        cur.execute("""
            SELECT id, ST_SetSRID(ST_MakePoint(lon, lat), 4326) AS geom
            FROM estaciones_bomberos
            ORDER BY ST_Distance(ST_SetSRID(ST_MakePoint(%s, %s), 4326), ST_SetSRID(ST_MakePoint(lon, lat), 4326))
            LIMIT 1;
        """, (emergency_lng, emergency_lat))
        fire_station = cur.fetchone()
        if not fire_station:
            print("No fire station found.")
            return jsonify({'error': 'No fire station found'}), 500
        print(f"Fire station found: {fire_station}")

        # Encontrar el nodo más cercano al punto de emergencia
        cur.execute("""
            SELECT id AS node_id
            FROM nodes
            ORDER BY geom <-> ST_SetSRID(ST_MakePoint(%s, %s), 4326)
            LIMIT 1;
        """, (emergency_lng, emergency_lat))
        emergency_node = cur.fetchone()
        if not emergency_node:
            print("No emergency node found.")
            return jsonify({'error': 'No emergency node found'}), 500
        print(f"Emergency node found: {emergency_node}")

        # Encontrar el nodo más cercano a la estación de bomberos
        cur.execute("""
            SELECT id AS node_id
            FROM nodes
            ORDER BY geom <-> %s
            LIMIT 1;
        """, (fire_station['geom'],))
        station_node = cur.fetchone()
        if not station_node:
            print("No station node found.")
            return jsonify({'error': 'No station node found'}), 500
        print(f"Station node found: {station_node}")

        # Ejecutar pgr_dijkstra para calcular la ruta
        cur.execute("""
            SELECT route.*, ST_AsGeoJSON(e.geom)::json AS geom
            FROM pgr_dijkstra(
                'SELECT id, source, target, cost, reverse_cost FROM edges',
                %s, %s, directed := true
            ) AS route
            JOIN edges AS e ON route.edge = e.id;
        """, (station_node['node_id'], emergency_node['node_id']))
        route_result = cur.fetchall()

        if not route_result:
            print("No route found.")
            return jsonify({'error': 'No route found'}), 500
        print(f"Route found with {len(route_result)} segments.")

        # Formatear los resultados de la ruta como GeoJSON
        route_geojson = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": row['geom'],  # Ahora en formato JSON
                    "properties": {
                        "seq": row['seq'],
                        "cost": row['cost'],
                        "agg_cost": row['agg_cost']
                    }
                } for row in route_result
            ]
        }

        cur.close()
        conn.close()

        return jsonify(route_geojson)


    except Exception as e:
        print(f"Error calculating route: {e}")
        return jsonify({'error': 'Unable to calculate route'}), 500

if __name__ == '__main__':
    app.run(debug=True)