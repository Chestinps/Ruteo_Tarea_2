import requests
import geojson
import time

def descargar_reductores_velocidad():
    # Query Overpass
    consulta = """
    area[name="Región Metropolitana de Santiago"]->.searchArea;
    node["traffic_calming"="bump"](area.searchArea);
    out body;
    """
    
    url = "http://overpass-api.de/api/interpreter"

    respuesta = requests.post(url, data={'data': consulta})
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        return datos
    else:
        print(f"Error al descargar datos: {respuesta.status_code}")
        return None

def guardar_geojson(datos, archivo_salida):
    features = []
    for elemento in datos['elements']:
        if elemento['type'] == 'node':
            punto = geojson.Point((elemento['lon'], elemento['lat']))
            feature = geojson.Feature(geometry=punto, properties=elemento.get('tags', {}))
            features.append(feature)
    
    coleccion = geojson.FeatureCollection(features)

    with open(archivo_salida, 'w') as archivo:
        geojson.dump(coleccion, archivo)
    
    print(f"Datos guardados en {archivo_salida}")

def main():
    print("Descargando reductores de velocidad...")
    datos = descargar_reductores_velocidad()
    
    if datos:
        archivo_salida = f"reductores_velocidad_santiago_{int(time.time())}.geojson"
        guardar_geojson(datos, archivo_salida)
    else:
        print("No se pudieron obtener los datos.")

if __name__ == "__main__":
    main()
