// Inicializar el mapa
var map = L.map('map').setView([-33.45, -70.65], 10); // Coordenadas de Santiago

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Variables para almacenar las capas de estaciones de bomberos, calles y ruta
let fireStationsLayer = null;
let streetsLayer = null;
let routeLayer = null;

// Cargar datos de estaciones de bomberos
function loadFireStations() {
    fetch('/data/fire_stations')
        .then(response => response.json())
        .then(data => {
            fireStationsLayer = L.geoJSON(data, {
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

// Función para cargar calles de la comuna seleccionada
function loadStreets() {
    const comuna = document.getElementById('comuna-select').value;
    const file = `/data/streets_${comuna}`;

    fetch(file)
        .then(response => response.json())
        .then(data => {
            if (streetsLayer) {
                map.removeLayer(streetsLayer);
            }
            streetsLayer = L.geoJSON(data, {
                style: { color: 'red', weight: 2, opacity: 1 }
            }).addTo(map);
        })
        .catch(error => console.error("Error loading streets:", error));
}

// Variables para el marcador de emergencia y la capa de ruta
let emergencyMarker = null;

// Evento click en el mapa para capturar coordenadas y mostrar marcador de "Emergencia"
map.on('click', function (e) {
    const coords = e.latlng;

    if (emergencyMarker) {
        map.removeLayer(emergencyMarker);
    }

    emergencyMarker = L.marker([coords.lat, coords.lng]).addTo(map)
        .bindPopup("Emergencia").openPopup();

    // Enviar coordenadas al servidor y solicitar la ruta
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
});