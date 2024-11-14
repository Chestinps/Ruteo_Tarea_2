// Inicializar el mapa
var map = L.map('map').setView([-33.45, -70.65], 10); // Coordenadas de Santiago

// Cargar el layer de OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Variable global para las estaciones de bomberos
let fireStationsLayer;

// Cargar los datos GeoJSON de estaciones de bomberos
function loadFireStations() {
    fetch('/data/fire_stations')
        .then(response => response.json())
        .then(data => {
            fireStationsLayer = L.geoJSON(data, {
                onEachFeature: function (feature, layer) {
                    layer.bindPopup('<strong>' + feature.properties.name + '</strong><br>' + feature.properties['addr:street']);
                }
            });
        })
        .catch(error => console.error('Error al cargar las estaciones de bomberos:', error));
}

// Lista de archivos GeoJSON de calles de las comunas
const streetsFiles = {
    "cerrillos": '/data/streets_cerrillos',
    "cerro_navia": '/data/streets_cerro_navia',
    "conchali": '/data/streets_conchalí',
    "el_bosque": '/data/streets_el_bosque',
    "estacion_central": '/data/streets_estación_central',
    "huechuraba": '/data/streets_huechuraba',
    "independencia": '/data/streets_independencia',
    "la_cisterna": '/data/streets_la_cisterna',
    "la_florida": '/data/streets_la_florida',
    "la_granja": '/data/streets_la_granja',
    "la_pintana": '/data/streets_la_pintana',
    "la_reina": '/data/streets_la_reina',
    "las_condes": '/data/streets_las_condes',
    "lo_barnechea": '/data/streets_lo_barnechea',
    "lo_espejo": '/data/streets_lo_espejo',
    "lo_prado": '/data/streets_lo_prado',
    "macul": '/data/streets_macul',
    "maipu": '/data/streets_maipú',
    "nuñoa": '/data/streets_ñuñoa',
    "pedro_aguirre_cerda": '/data/streets_pedro_aguirre_cerda',
    "peñalolén": '/data/streets_peñalolén',
    "providencia": '/data/streets_providencia',
    "pudahuel": '/data/streets_pudahuel',
    "puente_alto": '/data/streets_puente_alto',
    "quilicura": '/data/streets_quilicura',
    "quinta_normal": '/data/streets_quinta_normal',
    "recoleta": '/data/streets_recoleta',
    "renca": '/data/streets_renca',
    "san_joaquin": '/data/streets_san_joaquín',
    "san_miguel": '/data/streets_san_miguel',
    "san_ramón": '/data/streets_san_ramón',
    "santiago": '/data/streets_santiago',
    "vitacura": '/data/streets_vitacura'
};

// Cargar las calles de la comuna seleccionada
function loadStreets() {
    const comuna = document.getElementById('comuna-select').value; // Obtener comuna seleccionada
    const file = streetsFiles[comuna]; // Obtener archivo correspondiente

    if (file) {
        fetch(file)
            .then(response => response.json())
            .then(data => {
                L.geoJSON(data, {
                    style: {
                        color: 'red',
                        weight: 2
                    }
                }).addTo(map);
            })
            .catch(error => console.error('Error al cargar el archivo GeoJSON de calles:', error));
    } else {
        console.error("Comuna no encontrada:", comuna);
    }
}

// Cargar la ruta óptima (solo si el checkbox está marcado)
document.getElementById('toggleRoute').addEventListener('change', function () {
    if (this.checked) {
        // Lógica para cargar la ruta (en este ejemplo, no se tiene implementado)
    }
});

// Cargar las estaciones de bomberos y calles según el estado del checkbox
document.getElementById('toggleFireStations').addEventListener('change', function () {
    if (this.checked) {
        if (fireStationsLayer) {
            fireStationsLayer.addTo(map);  // Mostrar las estaciones de bomberos
        }
    } else {
        if (fireStationsLayer) {
            map.removeLayer(fireStationsLayer);  // Ocultar las estaciones de bomberos
        }
    }
});

document.getElementById('toggleStreets').addEventListener('change', function () {
    if (this.checked) {
        loadStreets();
    } else {
        // Eliminar las calles del mapa (esto podría ser más eficiente si usas un layerGroup para las calles)
    }
});

// Llamar a la función para cargar las estaciones de bomberos al cargar el mapa
loadFireStations();
