import os
import requests
import geojson
import xml.etree.ElementTree as ET

def descargar_estaciones_bomberos():
    # Query Overpass
    consulta = """
    area[name="Región Metropolitana de Santiago"]->.searchArea;
    node["amenity"="fire_station"](area.searchArea);
    out body;
    """

    url = "http://overpass-api.de/api/interpreter"
    respuesta = requests.post(url, data={'data': consulta})
    
    if respuesta.status_code == 200:
        try:
            # Intentar obtener los datos como JSON
            datos = respuesta.json()
            return datos
        except ValueError:
            # Si falla, intentar parsear como XML
            print("La respuesta no es un JSON, se intentará parsear como XML.")
            return parsear_xml(respuesta.text)
    else:
        print(f"Error al descargar datos: {respuesta.status_code}")
        return None

def parsear_xml(xml_data):
    root = ET.fromstring(xml_data)
    elements = []
    for node in root.findall('node'):
        element = {
            "id": node.get("id"),
            "lat": float(node.get("lat")),
            "lon": float(node.get("lon")),
            "tags": {tag.get("k"): tag.get("v") for tag in node.findall('tag')}
        }
        elements.append(element)
    return {'elements': elements}

def guardar_geojson(datos, archivo_salida):
    features = []
    for elemento in datos['elements']:
        punto = geojson.Point((elemento['lon'], elemento['lat']))
        feature = geojson.Feature(geometry=punto, properties=elemento.get('tags', {}))
        features.append(feature)
    
    coleccion = geojson.FeatureCollection(features)
    
    with open(archivo_salida, 'w') as archivo:
        geojson.dump(coleccion, archivo)
    
    print(f"Datos guardados en {archivo_salida}")

def main():
    print("Descargando estaciones de bomberos...")
    datos = descargar_estaciones_bomberos()
    
    if datos:
        # Obtener la ruta actual donde se encuentra el script estaciones.py
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Definir la ruta completa para el archivo GeoJSON
        archivo_salida = os.path.join(current_dir, "estaciones.geojson")
        
        # Guardar el archivo en la misma carpeta que estaciones.py
        guardar_geojson(datos, archivo_salida)
    else:
        print("No se pudieron obtener los datos.")

if __name__ == "__main__":
    main()
