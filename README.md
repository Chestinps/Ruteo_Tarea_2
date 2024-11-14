# Pasos

## Paso 1
Para iniciar la base de datos, se debe ingresar el comando:
sudo docker-compose up -d

Luego, para detener el servicio de PostgreSQL, usa:
sudo systemctl stop postgresql

Accede al contenedor de PostGIS con el siguiente comando:
sudo docker exec -it postgis-container bash

Para conectarte a la base de datos `ruteo_db`, utiliza:
psql -U admin -d ruteo_db

O también puedes hacerlo con este comando que accede directamente al contenedor y a la base de datos:
sudo docker exec -it postgis-container psql -U admin -d ruteo_db

Crear las tablas, debe ingresar a la carpeta scripts y ejecutar este comando:
psql -U admin -d ruteo_db -h localhost -p 5432 -f tablas.sql

Para ver las tablas disponibles, ingresa:
\dt

Para salir de la base de datos , ingresa: 
\q

## Paso 2

## Paso 3
