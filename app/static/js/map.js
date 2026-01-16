let map = L.map('map').setView([-8.83, 13.23], 13); // Default: Luanda
let markers = [];
let currentCoords = { lat: -8.83, lon: 13.23 };

// Camada de Mapa (Estilo Dark opcional se usar CartoDB)
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap &copy; CARTO'
}).addTo(map);

async function fetchATMs(lat, lon, search = '') {
    try {
        const response = await fetch(`/api/atms?lat=${lat}&lon=${lon}&search=${search}`);
        if (!response.ok) throw new Error('Erro ao carregar dados');

        const data = await response.json();

        // Limpar marcadores anteriores
        markers.forEach(m => map.removeLayer(m));
        markers = [];

        const list = document.getElementById('atm-list');
        list.innerHTML = '';

        if (data.length === 0) {
            list.innerHTML = '<p style="text-align:center; padding:20px;">Nenhum ATM encontrado.</p>';
            return;
        }

        data.forEach(atm => {
            // Criar marcador
            const marker = L.marker([atm.lat, atm.lon])
                .addTo(map)
                .bindPopup(`<b>${atm.bank_name}</b><br>${atm.address || 'Sem endereço'}`);

            markers.push(marker);

            // Adicionar à lista lateral
            const card = document.createElement('div');
            card.className = 'atm-card';
            card.innerHTML = `
                <strong>${atm.bank_name}</strong>
                <span style="display:block; font-size: 0.8em; color: #8b949e;">${atm.distance} km de distância</span>
            `;
            card.onclick = () => {
                map.flyTo([atm.lat, atm.lon], 17);
                marker.openPopup();
            };
            list.appendChild(card);
        });
    } catch (err) {
        console.error('Erro:', err);
    }
}

// Função para buscar quando o utilizador digita
function filterATMs() {
    const search = document.getElementById('searchInput').value;
    fetchATMs(currentCoords.lat, currentCoords.lon, search);
}

function updateLocation() {
    if (!navigator.geolocation) {
        alert("O seu navegador não suporta geolocalização.");
        fetchATMs(currentCoords.lat, currentCoords.lon);
        return;
    }

    navigator.geolocation.getCurrentPosition(
        pos => {
            currentCoords.lat = pos.coords.latitude;
            currentCoords.lon = pos.coords.longitude;

            map.setView([currentCoords.lat, currentCoords.lon], 15);

            // Adicionar marcador do utilizador (Azul)
            L.circleMarker([currentCoords.lat, currentCoords.lon], {
                color: '#58a6ff',
                radius: 8,
                fillOpacity: 0.8
            }).addTo(map).bindPopup("Você está aqui");

            fetchATMs(currentCoords.lat, currentCoords.lon);
        },
        err => {
            console.warn("Acesso ao GPS negado. Usando localização padrão.");
            fetchATMs(currentCoords.lat, currentCoords.lon);
        }
    );
}

// Event Listeners
document.addEventListener('DOMContentLoaded', updateLocation);

// Adicionar listener de busca com "debounce" (opcional) ou direto
document.getElementById('searchInput').addEventListener('input', filterATMs);