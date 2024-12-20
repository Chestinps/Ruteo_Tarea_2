import json
import psycopg2
import os
def cargar_lomos(cursor):
    # Ruta del archivo GeoJSON
    ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'Amenazas', 'reductores_velocidad.geojson')
    
    try:
        with open(ruta_archivo, 'r') as json_file:
            data = json.load(json_file)
            
            # Asegúrate de que 'features' esté en el json
            if 'features' in data:
                for item in data['features']:
                    # Verifica que 'geometry' y 'properties' estén presentes
                    if 'geometry' in item and 'properties' in item:
                        lat = item['geometry']['coordinates'][1]  # Latitud
                        lon = item['geometry']['coordinates'][0]  # Longitud
                        osm_id = item['properties'].get('id', None)
                        traffic_calming = item['properties'].get('traffic_calming', None)
                        
                        if lat is not None and lon is not None:
                            # Crear la geometría de tipo Point usando WKT (Well-Known Text)
                            geom_point = f"POINT({lon} {lat})"
                            
                            # Verificar si el osm_id ya existe en la tabla
                            cursor.execute("""
                                SELECT 1 FROM lomos WHERE osm_id = %s;
                            """, (osm_id,))
                            result = cursor.fetchone()
                            
                            # Si osm_id ya existe, no insertamos
                            if result:
                                print(f"Advertencia: El osm_id {osm_id} ya existe en la base de datos. No se insertará.")
                            else:
                                # Insertar en la base de datos
                                cursor.execute("""
                                    INSERT INTO lomos (osm_id, lat, lon, traffic_calming, geom)
                                    VALUES (%s, %s, %s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326));
                                """, (osm_id, lat, lon, traffic_calming, geom_point))
                        else:
                            print(f"Advertencia: Coordenadas faltantes para el elemento con id {osm_id}")
            else:
                print("Error: El archivo GeoJSON no contiene la clave 'features'.")
    
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {ruta_archivo}")
    except json.JSONDecodeError:
        print("Error: El archivo JSON está mal formado.")
    except Exception as e:
        print(f"Ocurrió un error al cargar lomos: {e}")
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
                
                # Extraer las coordenadas de lat y lon
                lat = element['geometry']['coordinates'][1]
                lon = element['geometry']['coordinates'][0]
                
                if lat is not None and lon is not None:
                    # Convertir las coordenadas a geometría Point (WKT)
                    geom_point = f"POINT({lon} {lat})"
                    
                    # Verificar si el osm_id ya existe en la tabla 'grifos'
                    osm_id = properties.get("id")
                    cursor.execute("""
                        SELECT 1 FROM grifos WHERE osm_id = %s;
                    """, (osm_id,))
                    result = cursor.fetchone()
                    
                    # Si osm_id ya existe, omitir la inserción
                    if not result:
                        # Insertar en la base de datos, incluyendo la geometría como tipo Point
                        cursor.execute("""
                            INSERT INTO grifos (osm_id, lat, lon, tags, geom)
                            VALUES (%s, %s, %s, %s, ST_SetSRID(ST_GeomFromText(%s), 4326));
                        """, (osm_id, lat, lon, json.dumps(properties), geom_point))
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {ruta_archivo}")
    except json.JSONDecodeError:
        print("Error: El archivo JSON está mal formado.")
    except Exception as e:
        print(f"Ocurrió un error al cargar grifos: {e}")

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
    ruta_archivo = os.path.join(os.path.dirname(__file__), '..', 'Metadata', 'calles.geojson')
    try:
        with open(ruta_archivo, 'r') as json_file:
            data = json.load(json_file)

            # Verificar si 'data' contiene la clave 'features'
            if isinstance(data, dict) and 'features' in data:
                features = data['features']
                if isinstance(features, list):
                    for feature in features:
                        # Validar que cada 'feature' sea un diccionario y tenga claves necesarias
                        if isinstance(feature, dict):
                            properties = feature.get('properties', {})
                            geometry = feature.get('geometry', {})

                            # Obtener propiedades relevantes
                            way_id = properties.get('way_id')
                            nodes = properties.get('nodes', [])
                            street_name = properties.get('street_name')
                            highway_type = properties.get('highway_type')
                            highway_value = properties.get('highway_value')

                            # Validar el valor de lanes (número de carriles)
                            lanes = properties.get('lanes')
                            if lanes is not None:
                                try:
                                    lanes = int(lanes)  # Convertir a entero
                                except ValueError:
                                    lanes = None  # Si no es un número, usar NULL

                            # Validar y convertir geometría a LINESTRING si es del tipo correcto
                            geom_type = geometry.get('type')
                            coordinates = geometry.get('coordinates', [])

                            if geom_type == "LineString" and isinstance(coordinates, list):
                                # Convertir coordenadas en formato WKT LINESTRING
                                geom_linestring = "LINESTRING(" + ", ".join(
                                    f"{lon} {lat}" for lon, lat in coordinates
                                ) + ")"

                                # Insertar en la base de datos, incluyendo la geometría
                                cursor.execute("""
                                    INSERT INTO tipos_calles (way_id, nodes, street_name, highway_type, highway_value, lanes, geom)
                                    VALUES (%s, %s, %s, %s, %s, %s, ST_GeomFromText(%s, 4326))
                                    ON CONFLICT (way_id) DO NOTHING;  -- Evita duplicados
                                """, (way_id, nodes, street_name, highway_type, highway_value, lanes, geom_linestring))
                            else:
                                print(f"Advertencia: Geometría no válida o faltante para el elemento con way_id {way_id}")
                        else:
                            print(f"Advertencia: Elemento inesperado en 'features': {feature}")
                else:
                    print("Error: La clave 'features' no contiene una lista.")
            else:
                print("Error: El archivo no contiene una clave 'features' o la estructura no es la esperada.")
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
