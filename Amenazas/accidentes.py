import requests
import json

# URL de la API
url = 'https://www.transporteinforma.cl/wp/wp-admin/admin-ajax.php'

# Cuerpo de la solicitud POST
data = {
    'action': 'home_incident_zone',
    'zone': 'zona-centro'
}

try:
    # Hacemos la petición POST
    response = requests.post(url, data=data)

    # Verificamos si la respuesta fue exitosa
    if response.status_code == 200:
        print("Respuesta exitosa!")

        # Obtenemos el contenido de la respuesta en formato JSON
        response_data = response.json()

        # Guardamos los datos en un archivo JSON
        with open('accidentes.json', 'w', encoding='utf-8') as json_file:
            json.dump(response_data, json_file, ensure_ascii=False, indent=4)
        
        print("Datos guardados en 'accidentes.json'")
    else:
        print(f"Error en la solicitud: {response.status_code}")

except Exception as e:
    print(f"Ocurrió un error: {e}")
