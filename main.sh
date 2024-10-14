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
estaciones_de_bomberos="Infraestructura/estaciones.py"
lomos_de_toro="Amenazas/lomos.py"
grifos="Metadata/grifos.py"

ejecutar_script $estaciones_de_bomberos
ejecutar_script $lomos_de_toro
ejecutar_script $grifos
