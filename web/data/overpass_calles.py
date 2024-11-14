import requests
import xmltodict
import json
import os

# Lista de comunas
comunas = [
    "Cerrillos", "Cerro Navia", "Conchalí", "El Bosque", "Estación Central", 
    "Huechuraba", "Independencia", "La Cisterna", "La Florida", "La Granja", 
    "La Pintana", "La Reina", "Las Condes", "Lo Barnechea", "Lo Espejo", 
    "Lo Prado", "Macul", "Maipú", "Ñuñoa", "Pedro Aguirre Cerda", 
    "Peñalolén", "Providencia", "Pudahuel", "Puente Alto", "Quilicura", 
    "Quinta Normal", "Recoleta", "Renca", "San Joaquín", "San Miguel", 
    "San Ramón", "Santiago", "Vitacura"
]

# URL de Overpass API
url = "http://overpass-api.de/api/interpreter"

# Directorio para guardar los archivos GeoJSON
output_dir = '../data'
os.makedirs(output_dir, exist_ok=True)

# Función para realizar la consulta y guardar el resultado en GeoJSON
def obtener_calles(comuna):
    consulta = f"""
    area[name="{comuna}"]->.searchArea;
    (
      way["highway"](area.searchArea);
    );
    out body;
    >;
    out skel qt;
    """
    
    # Realiza la solicitud POST
    respuesta = requests.post(url, data={'data': consulta})
    
    if respuesta.status_code == 200:
        # Convierte el XML en un diccionario de Python
        xml_data = respuesta.content
        json_data = xmltodict.parse(xml_data)
        
        # Procesa los elementos 'way' para construir el GeoJSON
        features = []
        if 'osm' in json_data:
            ways = json_data['osm'].get('way', [])
            nodes_dict = {node['@id']: (float(node['@lon']), float(node['@lat']))
                          for node in json_data['osm'].get('node', [])}
            
            for element in ways:
                # Extrae los nodos que conforman la vía
                nodes = element['nd']
                coordinates = [nodes_dict[node['@ref']] for node in nodes if node['@ref'] in nodes_dict]
                
                # Manejo de las etiquetas (tags)
                tags_data = element.get('tag', [])
                if isinstance(tags_data, dict):
                    tags_data = [tags_data]
                
                # Extrae los metadatos (tags) asociados con la calle
                tags = {tag['@k']: tag['@v'] for tag in tags_data}
                
                # Crea un objeto de tipo "Feature" para GeoJSON
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": coordinates
                    },
                    "properties": tags
                }
                features.append(feature)
        
        # Estructura el GeoJSON final
        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }
        
        # Guardamos el GeoJSON con el nombre de la comuna
        filename = f"streets_{comuna.replace(' ', '_').lower()}.geojson"
        with open(os.path.join(output_dir, filename), 'w') as f:
            json.dump(geojson_data, f, indent=4)
        
        print(f"Datos de {comuna} convertidos a GeoJSON y guardados en '{filename}'.")
    else:
        print(f"Error en la solicitud para {comuna}: {respuesta.status_code}")

# Ejecuta la función para cada comuna
for comuna in comunas:
    obtener_calles(comuna)