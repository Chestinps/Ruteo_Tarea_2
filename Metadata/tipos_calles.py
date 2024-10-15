import requests
import json

# URL de la API de Overpass
overpass_url = "http://overpass-api.de/api/interpreter"

# Consulta Overpass API
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

    # Guarda los resultados en un archivo JSON
    with open('santiago_highways.json', 'w') as f:
        json.dump(data, f, indent=4)
        
    print("Archivo JSON guardado como 'santiago_highways.json'")
    
    # Imprimir algunas de las etiquetas de los caminos encontrados (opcional)
    for element in data['elements']:
        if element['type'] == 'way':
            highway_type = element['tags'].get('highway', 'No Type')
            print(f"Way ID: {element['id']} | Highway Type: {highway_type}")
else:
    print(f"Error in request: {response.status_code}")
