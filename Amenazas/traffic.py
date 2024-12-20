import os
import requests
import json

def obtener_datos_trafico(api_key, version, style, zoom, output_format, coordinates, unit='KMPH', open_lr=False, output_file='trafico.json'):
    url = f"https://api.tomtom.com/traffic/services/{version}/flowSegmentData/{style}/{zoom}/{output_format}"

    params = {
        'key': api_key,
        'point': ','.join(map(str, coordinates)),
        'unit': unit,
        'openLr': str(open_lr).lower()
    }

    try:
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            # Obtener la ruta actual donde se encuentra el script traffic.py
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Definir la ruta completa para el archivo JSON
            json_path = os.path.join(current_dir, output_file)

            # Guardar el archivo en la misma carpeta que traffic.py
            with open(json_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            print(f"Datos guardados correctamente en {json_path}")

            flow_data = data.get('flowSegmentData', {})
            velocidad_actual = flow_data.get('currentSpeed')
            velocidad_flujo_libre = flow_data.get('freeFlowSpeed')
            tiempo_actual_viaje = flow_data.get('currentTravelTime')
            tiempo_flujo_libre = flow_data.get('freeFlowTravelTime')
            confianza = flow_data.get('confidence')
            cierre_carretera = flow_data.get('roadClosure', False)

            print(f"Velocidad actual: {velocidad_actual} km/h")
            print(f"Velocidad en flujo libre: {velocidad_flujo_libre} km/h")
            print(f"Tiempo actual de viaje: {tiempo_actual_viaje} segundos")
            print(f"Tiempo en flujo libre: {tiempo_flujo_libre} segundos")
            print(f"Confianza en los datos: {confianza}")
            print(f"¿Carretera cerrada?: {'Sí' if cierre_carretera else 'No'}")

        else:
            print(f"Error: {response.status_code}, no se pudo obtener datos de tráfico.")

    except Exception as e:
        print(f"Excepción ocurrió: {e}")


api_key = 'Iatx2R6bKqtQZ3noyVafNSgKba77gSMS'
version = '4'
style = 'relative0'
zoom = '10'
output_format = 'json'
coordinates = [52.41072, 4.84239]

# Ahora el archivo se guardará en la misma carpeta que el script
obtener_datos_trafico(api_key, version, style, zoom, output_format, coordinates)
