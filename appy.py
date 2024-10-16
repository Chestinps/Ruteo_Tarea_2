import os
import subprocess

# Obtener la ruta absoluta de la carpeta principal (donde está appy.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Definir las rutas a las subcarpetas
amenazas_dir = os.path.join(current_dir, 'Amenazas')
metadata_dir = os.path.join(current_dir, 'Metadata')
infraestructura_dir = os.path.join(current_dir, 'Infraestructura')
db_dir = os.path.join(current_dir, 'db')

# Función para ejecutar un script de Python
def ejecutar_script(script_path):
    try:
        print(f"Ejecutando {script_path}...")
        subprocess.run(["python3", script_path], check=True)
        print(f"Completado: {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {script_path}: {e}")

# Ejecutar los scripts en orden:

# Amenazas: accidentes.py, lomos.py, traffic.py
amenazas_scripts = ["accidentes.py", "lomos.py", "traffic.py"]
for script in amenazas_scripts:
    script_path = os.path.join(amenazas_dir, script)
    ejecutar_script(script_path)

# Metadata: grifos.py, tipos_calles.py
metadata_scripts = ["grifos.py", "tipos_calles.py"]
for script in metadata_scripts:
    script_path = os.path.join(metadata_dir, script)
    ejecutar_script(script_path)

# Infraestructura: estaciones.py
infraestructura_scripts = ["estaciones.py"]
for script in infraestructura_scripts:
    script_path = os.path.join(infraestructura_dir, script)
    ejecutar_script(script_path)

# Finalmente, ejecutar cargar_datos.py en la carpeta db
db_script = os.path.join(db_dir, "cargar_datos.py")
ejecutar_script(db_script)

print("Todos los scripts han sido ejecutados y los datos han sido cargados en la base de datos.")
