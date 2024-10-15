import requests
import geojson
import time
import xml.etree.ElementTree as ET

def descargar_grifos():
    # Query Overpass
    consulta = """
    area[name="Región Metropolitana de Santiago"]->.searchArea;
    node["emergency"="fire_hydrant"](area.searchArea);
    out body;
    """
    
    url = "http://overpass-api.de/api/interpreter"
    respuesta = requests.post(url, data={'data': consulta})
    
    if respuesta.status_code == 200:
        # Comprobar si la respuesta es XML
        try:
            # Intentar parsear la respuesta como JSON
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

# Función principal
def main():
    print("Descargando bocas de incendio...")
    datos = descargar_grifos()
    
    if datos:
        archivo_salida = f"grifos.geojson"
        guardar_geojson(datos, archivo_salida)
    else:
        print("No se pudieron obtener los datos.")

if __name__ == "__main__":
    main()
