#!/bin/bash

ejecutar_script() {
    local ruta_script=$1
    echo "Ejecutando: $ruta_script"
    python $ruta_script
    
    if [ $? -eq 0 ]; then
        echo "Completado: $ruta_script"
    else
        echo "Error al ejecutar $ruta_script"
    fi
}

# Rutas de los scripts
ruta_estaciones_bomberos="scripts/estaciones_bomberos/descargar_estaciones_bomberos.py"
ruta_reductores_velocidad="scripts/reductores_velocidad/descargar_reductores_velocidad.py"
ruta_bocas_incendio="scripts/bocas_incendio/descargar_bocas_incendio.py"

ejecutar_script $ruta_estaciones_bomberos
ejecutar_script $ruta_reductores_velocidad
ejecutar_script $ruta_bocas_incendio
