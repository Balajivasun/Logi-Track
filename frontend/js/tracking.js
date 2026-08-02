document.addEventListener('DOMContentLoaded', initTracking);

let map;
let markers = [];

async function initTracking() {
    // Initialize MapLibre GL JS with OpenStreetMap raster tiles
    map = new maplibregl.Map({
        container: 'map',
        style: {
            'version': 8,
            'sources': {
                'osm': {
                    'type': 'raster',
                    'tiles': [
                        'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
                        'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
                        'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png'
                    ],
                    'tileSize': 256,
                    'attribution': '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                }
            },
            'layers': [{
                'id': 'osm-layer',
                'type': 'raster',
                'source': 'osm',
                'minzoom': 0,
                'maxzoom': 19
            }]
        },
        center: [78.6569, 11.1271], // Center of Tamil Nadu
        zoom: 7
    });

    map.addControl(new maplibregl.NavigationControl());

    loadActiveVehicles();
    
    // Refresh every 10 seconds to simulate real-time tracking
    setInterval(loadActiveVehicles, 10000);
}

async function loadActiveVehicles() {
    try {
        const vehicles = await apiCall('/vehicles/?status=On Trip');
        updateMap(vehicles);
    } catch (error) {
        console.error('Failed to load active vehicles', error);
    }
}

function updateMap(vehicles) {
    // Clear old markers
    markers.forEach(m => m.remove());
    markers = [];

    const fleetList = document.getElementById('active-fleet-list');
    fleetList.innerHTML = '';

    if (vehicles.length === 0) {
        fleetList.innerHTML = '<p style="color:var(--text-muted); font-size:0.9rem;">No vehicles are currently on a trip.</p>';
        return;
    }

    // Tamil Nadu bounds for random mock coordinates for MVP demonstration
    // Since we don't have real GPS, we will generate fake coords around TN if they are empty
    vehicles.forEach(vehicle => {
        let lng = vehicle.current_lng;
        let lat = vehicle.current_lat;

        if (!lng || !lat) {
            // Mock random coords around Trichy/Madurai
            lng = 78.6569 + (Math.random() - 0.5) * 2;
            lat = 11.1271 + (Math.random() - 0.5) * 2;
        }

        // Add to Sidebar
        fleetList.innerHTML += `
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--border-color); padding-bottom:5px;">
                <span style="font-weight:500; color:var(--text-main);">${vehicle.vehicle_number}</span>
                <span style="color:var(--warning); font-size:0.8rem; font-weight:600;"><i class="fa-solid fa-circle"></i> In Transit</span>
            </div>
        `;

        // Create Marker
        const el = document.createElement('div');
        el.className = 'truck-marker';
        el.innerHTML = '<i class="fa-solid fa-truck"></i>';
        
        const popup = new maplibregl.Popup({ offset: 25 })
            .setHTML(`
                <h3 style="margin-bottom:5px;">${vehicle.vehicle_number}</h3>
                <p style="margin:0; font-size:0.9rem;">Type: ${vehicle.type}</p>
                <p style="margin:0; font-size:0.9rem; margin-top:5px; color:var(--warning);">Status: <strong>${vehicle.status}</strong></p>
            `);

        const marker = new maplibregl.Marker({element: el})
            .setLngLat([lng, lat])
            .setPopup(popup)
            .addTo(map);

        markers.push(marker);
    });
}
