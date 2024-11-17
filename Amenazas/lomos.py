import os
import requests
import xml.etree.ElementTree as ET
import json

# Obtener la ruta actual donde se encuentra el script lomos.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Definir la ruta completa para el archivo JSON
json_path = os.path.join(current_dir, 'reductores_velocidad.geojson')

# Definir la URL de la API de Overpass
overpass_url = "http://overpass-api.de/api/interpreter"

# Definir la consulta (Overpass QL)
overpass_query = """
area[name="Región Metropolitana de Santiago"]->.searchArea;
node["traffic_calming"="bump"](area.searchArea);
out body;
"""

# Realizar la solicitud HTTP a la API
response = requests.post(overpass_url, data={"data": overpass_query})

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Obtener el contenido de la respuesta en formato texto (XML)
    xml_data = response.text

    # Parsear el XML
    root = ET.fromstring(xml_data)

    # Crear una lista para almacenar los datos procesados
    bumps = {
        "type": "FeatureCollection",
        "features": []
    }

    # Recorrer los nodos en el XML
    for node in root.findall('node'):
        # Extraer información del nodo
        bump_id = node.get("id")
        lat = node.get("lat")
        lon = node.get("lon")
        
        # Crear la geometría WKT (Point)
        geom_point = f"POINT({lon} {lat})"
        
        # Crear un feature para cada bump
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(lon), float(lat)]  # Coordenadas como lista [lon, lat]
            },
            "properties": {
                "id": bump_id,
                "traffic_calming": "bump"
            }
        }

        # Añadir el feature a la lista de features
        bumps["features"].append(feature)

    # Guardar los datos procesados en un archivo GeoJSON
    with open(json_path, 'w') as json_file:
        json.dump(bumps, json_file, indent=4)

    print(f"Consulta exitosa. Datos guardados en '{json_path}'.")
else:
    print(f"Error en la consulta. Código de estado: {response.status_code}")
