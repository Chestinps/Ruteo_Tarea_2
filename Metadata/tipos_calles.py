import os
import requests
import json
from geojson import Feature, LineString, FeatureCollection

# URL de la API de Overpass
overpass_url = "http://overpass-api.de/api/interpreter"

# Consulta Overpass API optimizada para rutas
overpass_query = """
[out:json];
area[name="Región Metropolitana de Santiago"]->.searchArea;
(
  way["highway"](area.searchArea);
  node(w)->.nodes;
);
out body;
"""

# Realizar la solicitud a la API
response = requests.post(overpass_url, data={'data': overpass_query})

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()

    # Crear un diccionario para almacenar las coordenadas de los nodos
    node_coords = {element['id']: (element['lon'], element['lat']) for element in data['elements'] if element['type'] == 'node'}
    
    # Crear una lista para almacenar las features de GeoJSON
    features = []
    
    # Iterar por los elementos tipo "way" y convertirlos en LineStrings
    for element in data['elements']:
        if element['type'] == 'way':
            # Obtener las coordenadas de los nodos del "way"
            coordinates = [node_coords[node_id] for node_id in element['nodes'] if node_id in node_coords]
            
            # Crear un LineString con las coordenadas
            line_string = LineString(coordinates)
            
            # Crear una feature con las propiedades del "way"
            feature = Feature(geometry=line_string, properties={
                'way_id': element['id'],
                'street_name': element['tags'].get('name', 'Unknown'),
                'highway_type': element['tags'].get('highway', 'Unknown'),
                'lanes': element['tags'].get('lanes', 'Unknown')
            })
            
            # Agregar la feature a la lista de features
            features.append(feature)
    
    # Crear una FeatureCollection de GeoJSON
    feature_collection = FeatureCollection(features)
    
    # Obtener la ruta actual donde se encuentra el script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Definir la ruta completa para el archivo GeoJSON
    geojson_path = os.path.join(current_dir, 'calles.geojson')
    
    # Guardar los datos GeoJSON en un archivo
    with open(geojson_path, 'w') as geojson_file:
        json.dump(feature_collection, geojson_file, indent=4)
    
    print(f"Archivo GeoJSON guardado como '{geojson_path}'")

else:
    print(f"Error en la solicitud: {response.status_code}")