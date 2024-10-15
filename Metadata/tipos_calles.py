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
    
    # Guarda los resultados optimizados en un archivo JSON
    with open('calles.json', 'w') as f:
        json.dump(optimized_data, f, indent=4)
    
    print("Archivo optimizado guardado como 'santiago_highways_optimized.json'")
    
else:
    print(f"Error en la solicitud: {response.status_code}")
