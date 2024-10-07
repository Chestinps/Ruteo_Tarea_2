import requests
import geojson
import time


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

# Función principal
def main():
    print("Descargando bocas de incendio...")
    datos = descargar_grifos()
    
    if datos:
        archivo_salida = f"bocas_incendio_santiago_{int(time.time())}.geojson"
        guardar_geojson(datos, archivo_salida)
    else:
        print("No se pudieron obtener los datos.")

if __name__ == "__main__":
    main()
