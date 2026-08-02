let allVehicles = [];

document.addEventListener('DOMContentLoaded', () => {
    loadVehicles();

    document.getElementById('vehicle-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            vehicle_number: document.getElementById('veh-number').value,
            type: document.getElementById('veh-type').value,
            capacity: parseFloat(document.getElementById('veh-capacity').value),
            fuel_capacity: parseFloat(document.getElementById('veh-fuel').value),
            current_fuel: parseFloat(document.getElementById('veh-fuel').value) // Full tank by default
        };

        try {
            await apiCall('/vehicles/', 'POST', payload);
            showToast('Vehicle added successfully!', 'success');
            closeVehicleModal();
            loadVehicles();
        } catch (error) {
            showToast(error.message, 'error');
        }
    });

    document.getElementById('vehicle-search').addEventListener('input', (e) => {
        renderVehicles(e.target.value.toLowerCase());
    });
});

async function loadVehicles() {
    try {
        allVehicles = await apiCall('/vehicles/');
        renderVehicles();
    } catch (error) {
        showToast('Failed to load vehicles', 'error');
    }
}

function getImageForType(type) {
    const formatted = type.toLowerCase().replace(' ', '_');
    // We generated: lorry, container_truck, pickup, trailer.
    // Fallbacks for others
    if (['lorry', 'container_truck', 'pickup', 'trailer'].includes(formatted)) {
        return `assets/images/vehicles/${formatted}.png`;
    }
    return `assets/images/vehicles/lorry.png`; // Fallback
}

function getStatusBadge(status) {
    const clsMap = {
        'Available': 'status-available',
        'Assigned': 'status-assigned',
        'On Trip': 'status-ontrip',
        'Maintenance': 'status-maintenance'
    };
    const cssClass = clsMap[status] || 'status-maintenance';
    return `<span class="vehicle-status ${cssClass}">${status}</span>`;
}

function renderVehicles(searchQuery = '') {
    const grid = document.getElementById('vehicle-grid');
    grid.innerHTML = '';

    const filtered = allVehicles.filter(v => 
        v.vehicle_number.toLowerCase().includes(searchQuery) ||
        v.type.toLowerCase().includes(searchQuery)
    );

    if (filtered.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding: 3rem; color:var(--text-muted);">
            <i class="fa-solid fa-truck" style="font-size:3rem; margin-bottom:1rem; opacity:0.5;"></i>
            <p>No vehicles found.</p>
        </div>`;
        return;
    }

    filtered.forEach(vehicle => {
        const card = document.createElement('div');
        card.className = 'vehicle-card slide-up';
        
        card.innerHTML = `
            <img src="${getImageForType(vehicle.type)}" alt="${vehicle.type}" class="vehicle-img" onerror="this.src='https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80'">
            <div class="vehicle-info">
                <div style="display:flex; justify-content:space-between; align-items:start;">
                    <div>
                        <h3>${vehicle.vehicle_number}</h3>
                        <div class="vehicle-type">${vehicle.type}</div>
                    </div>
                    ${getStatusBadge(vehicle.status)}
                </div>
                
                <div class="vehicle-stats">
                    <div><i class="fa-solid fa-weight-hanging"></i> ${vehicle.capacity} Tons</div>
                    <div><i class="fa-solid fa-gas-pump"></i> ${vehicle.current_fuel}/${vehicle.fuel_capacity} L</div>
                </div>

                <div class="vehicle-actions">
                    <button class="btn-outline" onclick="viewDetails(${vehicle.id})">Details</button>
                    <button class="btn-delete" onclick="deleteVehicle(${vehicle.id}, '${vehicle.status}')"><i class="fa-solid fa-trash"></i></button>
                </div>
            </div>
        `;
        grid.appendChild(card);
    });
}

async function deleteVehicle(id, status) {
    if (status === 'On Trip' || status === 'Assigned') {
        showToast('Cannot delete a vehicle that is currently assigned to a trip.', 'error');
        return;
    }
    
    if (confirm('Are you sure you want to delete this vehicle?')) {
        try {
            await apiCall(`/vehicles/${id}`, 'DELETE');
            showToast('Vehicle removed.', 'success');
            loadVehicles();
        } catch (error) {
            showToast(error.message, 'error');
        }
    }
}

function viewDetails(id) {
    // Placeholder for details page
    showToast('Vehicle details coming soon.', 'info');
}
