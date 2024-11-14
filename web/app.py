from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

# Ruta para servir la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para servir los datos GeoJSON de estaciones de bomberos
@app.route('/data/fire_stations')
def fire_stations():
    geojson_path = os.path.join(app.root_path, 'data', 'fire_stations.geojson')
    with open(geojson_path) as f:
        data = json.load(f)  # Leer como JSON
    return jsonify(data)

# Ruta dinámica para servir los datos GeoJSON de las calles de las comunas
@app.route('/data/streets_<comuna>')
def streets(comuna):
    # Convertir la comuna a minúsculas y reemplazar espacios por guiones bajos
    comuna_file = f"streets_{comuna.lower().replace(' ', '_')}.geojson"
    geojson_path = os.path.join(app.root_path, 'data', comuna_file)
    
    # Verificar si el archivo existe
    if os.path.exists(geojson_path):
        with open(geojson_path) as f:
            data = json.load(f)  # Leer como JSON
        return jsonify(data)
    else:
        return jsonify({'error': 'Archivo no encontrado'}), 404

# Ruta para servir la ruta generada con pgr_dijkstra
@app.route('/data/ruta')
def ruta_optima():
    geojson_path = os.path.join(app.root_path, 'data', 'ruta.geojson')
    with open(geojson_path) as f:
        data = json.load(f)  # Leer como JSON
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
