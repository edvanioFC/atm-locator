// Definições de Mapa
const defaultCoords = { lat: -8.83, lon: 13.23 };
let currentCoords = { ...defaultCoords };
let map, userMarker, routingControl;
let markers = [];

// Ícone para a localização do utilizador
const greenIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// Camadas de Mapa (Tiles)
const osm = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
});

const satellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

const dark = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO'
});

const googleStreets = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',{
    maxZoom: 20,
    subdomains:['mt0','mt1','mt2','mt3']
});

const baseMaps = {
    "Google Streets": googleStreets,
    "Padrão": osm,
    "Satélite": satellite,
    "Escuro": dark
};

/**
 * Inicia o mapa e os seus componentes.
 */
function initializeMap() {
    map = L.map('map', {
        center: [defaultCoords.lat, defaultCoords.lon],
        zoom: 13,
        layers: [googleStreets] // Camada padrão alterada para Google Streets (mais colorido)
    });

    L.control.layers(baseMaps).addTo(map);

    // Cria o marcador do utilizador na localização padrão inicial
    userMarker = L.marker([defaultCoords.lat, defaultCoords.lon], {
        icon: greenIcon,
        zIndexOffset: 1000 // Garante que o pino do user fique sempre por cima
    }).addTo(map).bindPopup("A carregar a sua localização...");

    if (!navigator.geolocation) {
        alert("O seu navegador não suporta geolocalização.");
        userMarker.getPopup().setContent("Geolocalização não suportada.").openPopup();
        fetchATMs(defaultCoords.lat, defaultCoords.lon);
        return;
    }

    navigator.geolocation.getCurrentPosition(
        pos => {
            currentCoords = { lat: pos.coords.latitude, lon: pos.coords.longitude };
            map.setView([currentCoords.lat, currentCoords.lon], 16);
            userMarker.setLatLng([currentCoords.lat, currentCoords.lon]).getPopup().setContent("Você está aqui");
            fetchATMs(currentCoords.lat, currentCoords.lon);
            startRealtimeTracking();
        },
        err => {
            console.warn(`Acesso ao GPS negado (Erro: ${err.message}). Usando localização padrão.`);
            userMarker.getPopup().setContent("Não foi possível obter a sua localização.").openPopup();
            fetchATMs(defaultCoords.lat, defaultCoords.lon);
        }
    );
}

/**
 * Busca e exibe os ATMs no mapa e na lista.
 */
async function fetchATMs(lat, lon, search = '') {
    try {
        const response = await fetch(`/api/atms?lat=${lat}&lon=${lon}&search=${search}`);
        if (!response.ok) throw new Error('Erro ao carregar dados dos ATMs');
        
        const data = await response.json();

        markers.forEach(m => map.removeLayer(m));
        markers = [];

        const list = document.getElementById('atm-list');
        list.innerHTML = '';

        if (data.length === 0) {
            list.innerHTML = '<div class="list-group-item">Nenhum ATM encontrado.</div>';
            return;
        }

        data.forEach(atm => {
            const popupContent = `<b>${atm.bank_name}</b><br>${atm.address || 'Sem endereço'}<br><button onclick="startRouting(${atm.lat}, ${atm.lon})" class="btn btn-primary btn-sm mt-2">Traçar Rota</button>`;
            const marker = L.marker([atm.lat, atm.lon]).addTo(map).bindPopup(popupContent);
            markers.push(marker);

            const card = document.createElement('a');
            card.href = "#";
            card.className = 'list-group-item list-group-item-action';
            card.innerHTML = `
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">${atm.bank_name}</h5>
                    <small>${atm.distance} km</small>
                </div>
                <p class="mb-1">${atm.address || 'Endereço não disponível'}</p>
            `;
            card.onclick = (e) => {
                e.preventDefault();
                map.flyTo([atm.lat, atm.lon], 17);
                marker.openPopup();
            };
            list.appendChild(card);
        });
    } catch (err) {
        console.error('Erro:', err);
        document.getElementById('atm-list').innerHTML = '<div class="list-group-item text-danger">Erro ao carregar ATMs.</div>';
    }
}

/**
 * Inicia o traçado da rota a partir da localização atual do utilizador até o multibanco.
 */
function startRouting(lat, lon) {
    if (routingControl) {
        map.removeControl(routingControl);
    }
    routingControl = L.Routing.control({
        waypoints: [
            L.latLng(currentCoords.lat, currentCoords.lon),
            L.latLng(lat, lon)
        ],
        routeWhileDragging: true,
        show: false,
        addWaypoints: false,
        draggableWaypoints: false,
        fitSelectedRoutes: true,
        lineOptions: {
            styles: [{ color: '#0d6efd', opacity: 0.8, weight: 6 }]
        },
        createMarker: function(i, waypoint, n) {
            // Não cria marcador para o ponto de partida (índice 0)
            if (i === 0) {
                return null; // Mantém o userMarker verde visível
            }
            // Cria marcador padrão para os outros pontos
            return L.marker(waypoint.latLng);
        }
    }).addTo(map);

    routingControl.on('routesfound', function(e) {
        const routes = e.routes;
        const summary = routes[0].summary;
        const timeMinutes = Math.round(summary.totalTime / 60);
        const distanceKm = (summary.totalDistance / 1000).toFixed(1);

        L.popup()
            .setLatLng([lat, lon])
            .setContent(`<b>Tempo estimado: ${timeMinutes} min</b><br>Distância: ${distanceKm} km`)
            .openOn(map);
    });
}

/**
 * Inicia o rastreamento em tempo real da localização do utilizador.
 */
function startRealtimeTracking() {
    navigator.geolocation.watchPosition(
        pos => {
            currentCoords = { lat: pos.coords.latitude, lon: pos.coords.longitude };
            userMarker.setLatLng([currentCoords.lat, currentCoords.lon]);
            if (routingControl) {
                routingControl.spliceWaypoints(0, 1, L.latLng(currentCoords.lat, currentCoords.lon));
            }
        },
        err => console.warn(`Erro no watchPosition: ${err.message}`),
        { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
    );
}

function filterATMs() {
    const search = document.getElementById('searchInput').value;
    fetchATMs(currentCoords.lat, currentCoords.lon, search);
}

function recenterMap() {
    map.flyTo([currentCoords.lat, currentCoords.lon], 15);
}

// Event Listeners
document.addEventListener('DOMContentLoaded', initializeMap);
document.getElementById('searchInput').addEventListener('input', filterATMs);
