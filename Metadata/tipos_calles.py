import os
import requests
import json

# URL de la API de Overpass
overpass_url = "http://overpass-api.de/api/interpreter"

# Consulta Overpass API optimizada para rutas
overpass_query = """
[out:json];
area[name="Región Metropolitana de Santiago"]->.searchArea;
(
  way["highway"](area.searchArea);
);
out body;
>;
out skel qt;
"""

# Realizar la solicitud a la API
response = requests.post(overpass_url, data={'data': overpass_query})

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    data = response.json()
    
    # Crear una lista optimizada con los datos relevantes
    optimized_data = []
    
    for element in data['elements']:
        if element['type'] == 'way':
            way_info = {
                'way_id': element['id'],
                'nodes': element['nodes'],  # Puntos geográficos
                'street_name': element['tags'].get('name', 'Unknown'),  # Nombre de la calle
                'highway_type': element['tags'].get('highway', 'Unknown'),  # Tipo de calle
                'highway_value': element['tags'].get('highway'),  # Valor específico de 'highway' (e.g., secondary)
                'lanes': element['tags'].get('lanes', 'Unknown')  # Número de carriles
            }
            optimized_data.append(way_info)
    
    # Obtener la ruta actual donde se encuentra el script tipos_calles.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Definir la ruta completa para el archivo JSON
    json_path = os.path.join(current_dir, 'calles.json')
    
    # Guardar los resultados optimizados en un archivo JSON en la misma carpeta
    with open(json_path, 'w') as f:
        json.dump(optimized_data, f, indent=4)
    
    print(f"Archivo optimizado guardado como '{json_path}'")
    
else:
    print(f"Error en la solicitud: {response.status_code}")
