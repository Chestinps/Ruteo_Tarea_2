# Pasos para Configurar y Ejecutar el Proyecto

## Paso 1: Creación del Ambiente Virtual e Instalación de Dependencias
1. **Crear el ambiente virtual:**  
   `python3 -m venv venv`

2. **Activar el ambiente virtual:**  
   `source venv/bin/activate`

3. **Instalar las dependencias desde `requirements.txt`:**  
   `pip install -r requirements.txt`

---

## Paso 2: Configuración y Uso de la Base de Datos
1. **Iniciar la Base de Datos con Docker:**  
   - Para iniciar la base de datos:  
     `sudo docker-compose up -d`
   - Para detener el servicio de PostgreSQL en el sistema (si está corriendo en segundo plano):  
     `sudo systemctl stop postgresql`

2. **Acceder al Contenedor de PostGIS:**  
   - Accede al contenedor:  
     `sudo docker exec -it postgis-container bash`
   - Conéctate a la base de datos `ruteo_db`:  
     `psql -U admin -d ruteo_db`
   - Alternativamente, puedes usar este comando para conectarte directamente al contenedor y a la base de datos:  
     `sudo docker exec -it postgis-container psql -U admin -d ruteo_db`

3. **Crear las Tablas:**  
   - Navega a la carpeta `scripts` y ejecuta el siguiente comando:  
     `psql -U admin -d ruteo_db -h localhost -p 5432 -f tablas.sql`  
     *Nota: La contraseña del usuario `admin` es `admin123`.*

4. **Verificar Tablas y Salir:**  
   - Para listar las tablas disponibles:  
     `\dt`
   - Para salir de la base de datos:  
     `\q`

---

## Paso 3: Generación de Archivos JSON
1. Ejecuta los siguientes scripts en orden:  
   - `calles.py`  
   - `nodos.py`

2. Ingresa a la base de datos y crea el siguiente índice para optimizar la búsqueda:  
   `CREATE INDEX idx_nodes_lat_lon ON nodes(lat, lon);`

3. Ejecuta el script:  
   - `edges.py`
4. Ejecuta los siguientes scripts en orden:  
   - `appy.py`  
   - `cargar_datos.py`
---

## Paso 4: Montar la Web
1. Ejecuta el script `overpass_calles.py`.
2. Ejecuta el script `appy.py` para iniciar la web.
