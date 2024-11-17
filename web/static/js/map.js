// Inicializar el mapa
var map = L.map('map').setView([-33.45, -70.65], 10); // Coordenadas de Santiago

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Variables para almacenar las capas de estaciones de bomberos, calles y ruta
let fireStationsLayer = null;
let grifosLayer = null;
let lomosLayer = null;
let streetsLayer = null;
let routeLayer = null;
let routeMetadata = null;

// Lista de archivos GeoJSON de calles de las comunas
const streetsFiles = {
    "cerrillos": '/data/streets_cerrillos.geojson',
    "cerro_navia": '/data/streets_cerro_navia.geojson',
    "conchali": '/data/streets_conchalí.geojson',
    "el_bosque": '/data/streets_el_bosque.geojson',
    "estacion_central": '/data/streets_estación_central.geojson',
    "huechuraba": '/data/streets_huechuraba.geojson',
    "independencia": '/data/streets_independencia.geojson',
    "la_cisterna": '/data/streets_la_cisterna.geojson',
    "la_florida": '/data/streets_la_florida.geojson',
    "la_granja": '/data/streets_la_granja.geojson',
    "la_pintana": '/data/streets_la_pintana.geojson',
    "la_reina": '/data/streets_la_reina.geojson',
    "las_condes": '/data/streets_las_condes.geojson',
    "lo_barnechea": '/data/streets_lo_barnechea.geojson',
    "lo_espejo": '/data/streets_lo_espejo.geojson',
    "lo_prado": '/data/streets_lo_prado.geojson',
    "macul": '/data/streets_macul.geojson',
    "maipu": '/data/streets_maipú.geojson',
    "nuñoa": '/data/streets_ñuñoa.geojson',
    "pedro_aguirre_cerda": '/data/streets_pedro_aguirre_cerda.geojson',
    "penalolen": '/data/streets_peñalolén.geojson',
    "providencia": '/data/streets_providencia.geojson',
    "pudahuel": '/data/streets_pudahuel.geojson',
    "puente_alto": '/data/streets_puente_alto.geojson',
    "quilicura": '/data/streets_quilicura.geojson',
    "quinta_normal": '/data/streets_quinta_normal.geojson',
    "recoleta": '/data/streets_recoleta.geojson',
    "renca": '/data/streets_renca.geojson',
    "san_joaquin": '/data/streets_san_joaquín.geojson',
    "san_miguel": '/data/streets_san_miguel.geojson',
    "san_ramon": '/data/streets_san_ramón.geojson',
    "santiago": '/data/streets_santiago.geojson',
    "vitacura": '/data/streets_vitacura.geojson'
};        

const grifoIcon = L.icon({
    iconUrl: '/static/img/grifo.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
});

const lomoIcon = L.icon({
    iconUrl: '/static/img/lomo.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
});

const estacionIcon = L.icon({
    iconUrl: '/static/img/station.png',
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
});


// Cargar datos de estaciones de bomberos
function loadFireStations() {
    fetch('/data/fire_stations')
        .then(response => response.json())
        .then(data => {
            fireStationsLayer = L.geoJSON(data, {
                pointToLayer: function (feature, latlng) {
                    return L.marker(latlng, { icon: estacionIcon }); // Usa el ícono personalizado
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(feature.properties.name || "Estación de Bomberos");
                }
            }).addTo(map);
        })
        .catch(error => console.error("Error loading fire stations:", error));
}

// Alternar la visibilidad de las estaciones de bomberos
document.getElementById('toggleFireStations').addEventListener('change', function () {
    if (this.checked) {
        if (!fireStationsLayer) {
            loadFireStations();
        } else {
            map.addLayer(fireStationsLayer);
        }
    } else {
        if (fireStationsLayer) {
            map.removeLayer(fireStationsLayer);
        }
    }
});

if (document.getElementById('toggleFireStations').checked) {
    loadFireStations();
}


function loadGrifos() {
    fetch('/data/grifos')
        .then(response => response.json())
        .then(data => {
            grifosLayer = L.geoJSON(data, {
                pointToLayer: function (feature, latlng) {
                    return L.marker(latlng, { icon: grifoIcon });
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(feature.properties.name || "Grifo");
                }
            }).addTo(map);
        })
        .catch(error => console.error("Error loading grifos:", error));
}

document.getElementById('toggleGrifos').addEventListener('change', function () {
    if (this.checked) {
        if (!grifosLayer) {
            loadGrifos();
        } else {
            map.addLayer(grifosLayer);
        }
    } else {
        if (grifosLayer) {
            map.removeLayer(grifosLayer);
        }
    }
});

if (document.getElementById('toggleGrifos').checked) {
    loadGrifos();
}

function loadLomos() {
    fetch('/data/lomos')
        .then(response => response.json())
        .then(data => {
            lomosLayer = L.geoJSON(data, {
                pointToLayer: function (feature, latlng) {
                    return L.marker(latlng, { icon: lomoIcon });
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(feature.properties.name || "Lomo de Toro");
                }
            }).addTo(map);
        })
        .catch(error => console.error("Error loading lomos:", error));
}

document.getElementById('toggleLomos').addEventListener('change', function () {
    if (this.checked) {
        if (!lomosLayer) {
            loadLomos();
        } else {
            map.addLayer(lomosLayer);
        }
    } else {
        if (lomosLayer) {
            map.removeLayer(lomosLayer);
        }
    }
});

if (document.getElementById('toggleLomos').checked) {
    loadLomos();
}

// Función para cargar calles de la comuna seleccionada
function loadStreets() {
    const comuna = document.getElementById('comuna-select').value;
    const file = streetsFiles[comuna]; // Utilizar el archivo adecuado para la comuna seleccionada

    if (!file) {
        console.error("No se encontró un archivo para la comuna seleccionada:", comuna);
        return;
    }

    // Eliminar la capa de calles anterior si existe
    if (streetsLayer) {
        map.removeLayer(streetsLayer);
    }

    fetch(file)
        .then(response => response.json())
        .then(data => {
            // Añadir la nueva capa de calles al mapa
            streetsLayer = L.geoJSON(data, {
                style: { color: 'red', weight: 2, opacity: 1 }
            }).addTo(map);
        })
        .catch(error => console.error("Error al cargar las calles:", error));
}
// Variables para el marcador de emergencia y la capa de ruta
let emergencyMarker = null;

// Evento click en el mapa para capturar coordenadas y mostrar marcador de "Emergencia"
map.on('click', function (e) {
    const coords = e.latlng;

    document.getElementById('source-latitude').value = coords.lat;
    document.getElementById('source-longitude').value = coords.lng;
    document.getElementById('destination-latitude').value = coords.lat;
    document.getElementById('destination-longitude').value = coords.lng;

    if (emergencyMarker) {
        map.removeLayer(emergencyMarker);
    }

    emergencyMarker = L.marker([coords.lat, coords.lng]).addTo(map)
        .bindPopup("Emergencia").openPopup();

    // Llamada a la ruta /set_emergency
    fetch('/set_emergency', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: coords.lat, longitude: coords.lng })
    })
    .then(response => response.json())
    .then(data => {
        if (routeLayer) {
            map.removeLayer(routeLayer);
        }
        routeLayer = L.geoJSON(data, {
            style: { color: 'blue', weight: 4, opacity: 0.7 }
        }).addTo(map);
    })
    .catch(error => console.error("Error calculating route:", error));

    // Llamada a la ruta /set_route_metadata
    fetch('/set_route_metadata', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ latitude: coords.lat, longitude: coords.lng })
    })
    .then(response => response.json())
    .then(data => {
        if (routeMetadata) {
            map.removeLayer(routeMetadata);
        }
        routeMetadata = L.geoJSON(data, {
            style: { color: 'green', weight: 4, opacity: 0.7 }
        }).addTo(map);
    })
    .catch(error => console.error("Error calculating route metadata:", error));
});
