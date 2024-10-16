import json
import psycopg2
import os

def cargar_lomos(cursor):
    ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'Amenazas', 'reductores_velocidad.json')
    try:
        with open(ruta_archivo, 'r') as json_file:
            data = json.load(json_file)
            for item in data:
                cursor.execute("""
                    INSERT INTO lomos (osm_id, lat, lon, traffic_calming)
                    VALUES (%s, %s, %s, %s);
                """, (item["id"], item["lat"], item["lon"], item["traffic_calming"]))
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {ruta_archivo}")

def cargar_accidentes(cursor):
    ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'Amenazas', 'accidentes.json')
    try:
        with open(ruta_archivo, 'r') as json_file:
            data = json.load(json_file)
            if 'data' in data and isinstance(data['data'], list):  # Verifica que 'data' esté presente y sea una lista
                for item in data['data']:
                    if isinstance(item, dict):  # Asegúrate de que cada item sea un diccionario
                        cursor.execute("""
                            INSERT INTO accidentes (tipo, lat, lon, descripcion)
                            VALUES (%s, %s, %s, %s);
                        """, (
                            item.get("post_title"),  # Cambiar "tipo" por el campo adecuado, por ejemplo "post_title"
                            None,  # Aquí debes determinar cómo extraer las coordenadas lat y lon, si están disponibles
                            None,
                            item.get("post_content")  # Asumimos que "descripcion" se refiere a "post_content"
                        ))
            else:
                print("Error: El archivo no contiene una lista de diccionarios en la clave 'data'.")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {ruta_archivo}")
    except json.JSONDecodeError:
        print("Error: El archivo JSON está mal formado.")

def cargar_estaciones_bomberos(cursor):
    ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'Infraestructura', 'estaciones.geojson')
    try:
        with open(ruta_archivo, 'r') as json_file:
            data = json.load(json_file)
            for element in data['features']:
                properties = element['properties']
                cursor.execute("""
                    INSERT INTO estaciones_bomberos (osm_id, lat, lon, tags)
                    VALUES (%s, %s, %s, %s);
                """, (properties.get("id"), element['geometry']['coordinates'][1], element['geometry']['coordinates'][0], json.dumps(properties)))
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {ruta_archivo}")

def cargar_grifos(cursor):
    ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'Metadata', 'grifos.geojson')
    try:
        with open(ruta_archivo, 'r') as json_file:
            data = json.load(json_file)
            for element in data['features']:
                properties = element['properties']
                cursor.execute("""
                    INSERT INTO grifos (osm_id, lat, lon, tags)
                    VALUES (%s, %s, %s, %s);
                """, (properties.get("id"), element['geometry']['coordinates'][1], element['geometry']['coordinates'][0], json.dumps(properties)))
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {ruta_archivo}")

def cargar_trafico(cursor):
    # Construir la ruta del archivo
    ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'Amenazas', 'trafico.json')

    try:
        with open(ruta_archivo, 'r') as json_file:
            datos = json.load(json_file)

            # Acceder a 'flowSegmentData'
            flow_segment_data = datos.get('flowSegmentData', {})
            print(f"Tipo de flow_segment_data: {type(flow_segment_data)}")  # Para verificar el tipo

            if isinstance(flow_segment_data, dict):
                # Obtener las coordenadas
                coordinates = flow_segment_data.get('coordinates', {}).get('coordinate', [])
                for coord in coordinates:
                    lat = coord.get('latitude')
                    lon = coord.get('longitude')
                    
                    # Verificar que las coordenadas no sean nulas antes de insertar
                    if lat is not None and lon is not None:
                        cursor.execute("""
                            INSERT INTO trafico (coordinates, current_speed, free_flow_speed, current_travel_time, free_flow_travel_time, confidence, road_closure)
                            VALUES (ST_MakePoint(%s, %s), %s, %s, %s, %s, %s, %s)
                        """, (lon, lat, 
                              flow_segment_data.get('currentSpeed'), 
                              flow_segment_data.get('freeFlowSpeed'), 
                              flow_segment_data.get('currentTravelTime'), 
                              flow_segment_data.get('freeFlowTravelTime'), 
                              flow_segment_data.get('confidence'), 
                              flow_segment_data.get('roadClosure')))
                    else:
                        print("Coordenadas nulas, omitiendo...")
    except FileNotFoundError as e:
        print(f"Error: {e}. Asegúrate de que el archivo existe en la ruta especificada.")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el archivo JSON: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def cargar_tipos_calles(cursor):
    ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'Metadata', 'calles.json')
    try:
        with open(ruta_archivo, 'r') as json_file:
            data = json.load(json_file)
            for calle in data:
                way_id = calle['way_id']
                nodes = calle['nodes']
                street_name = calle['street_name']
                highway_type = calle['highway_type']
                highway_value = calle['highway_value']
                lanes = calle['lanes']

                # Crear la consulta SQL para insertar en la tabla tipos_calles
                cursor.execute("""
                    INSERT INTO tipos_calles (way_id, nodes, street_name, highway_type, highway_value, lanes)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (way_id) DO NOTHING;  -- Evita duplicados
                """, (way_id, nodes, street_name, highway_type, highway_value, lanes))
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {ruta_archivo}")
    except json.JSONDecodeError:
        print(f"Error: El archivo JSON está mal formado.")
    except Exception as e:
        print(f"Ocurrió un error al cargar tipos_calles: {e}")


def main():
    # Conectar a la base de datos
    conn = psycopg2.connect(
        dbname="ruteo_db",
        user="admin",
        password="admin123",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    # Cargar datos
    cargar_lomos(cursor)
    cargar_accidentes(cursor)
    cargar_estaciones_bomberos(cursor)
    cargar_grifos(cursor)
    cargar_trafico(cursor)
    cargar_tipos_calles(cursor) 

    # Hacer commit de los cambios y cerrar conexión
    conn.commit()
    cursor.close()
    conn.close()

    print("Datos cargados exitosamente en la base de datos.")

if __name__ == "__main__":
    main()
