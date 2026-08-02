document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const vehicleId = urlParams.get('id');
    
    if (!vehicleId) {
        window.location.href = 'vehicles.html';
        return;
    }
    
    loadVehicleDetails(vehicleId);
});

function switchTab(tabId) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(`tab-${tabId}`).classList.add('active');
}

async function loadVehicleDetails(id) {
    try {
        const vehicle = await apiCall(`/vehicles/${id}`);
        
        document.getElementById('v-number').textContent = vehicle.vehicle_number;
        document.getElementById('v-category').textContent = vehicle.category;
        document.getElementById('v-status').textContent = vehicle.status;
        
        let imgUrl = 'https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?auto=format&fit=crop&w=800&q=80';
        if (vehicle.category === 'Lorry') imgUrl = 'https://images.unsplash.com/photo-1592838064575-70ed626d3a0e?auto=format&fit=crop&w=800&q=80';
        if (vehicle.category === 'Pickup') imgUrl = 'https://images.unsplash.com/photo-1620023604313-05b6fa14c197?auto=format&fit=crop&w=800&q=80';
        if (vehicle.category === 'Tanker') imgUrl = 'https://images.unsplash.com/photo-1591784918451-4081c7e937d2?auto=format&fit=crop&w=800&q=80';
        document.getElementById('v-image').src = imgUrl;

        // Specs
        document.getElementById('s-man').textContent = vehicle.manufacturer;
        document.getElementById('s-mod').textContent = vehicle.model;
        document.getElementById('s-year').textContent = vehicle.manufacturing_year;
        document.getElementById('s-fuel-type').textContent = vehicle.fuel_type;
        document.getElementById('s-cap').textContent = vehicle.fuel_capacity;
        document.getElementById('s-cur').textContent = vehicle.current_fuel;
        document.getElementById('s-odo').textContent = vehicle.odometer_reading;
        document.getElementById('s-mil').textContent = vehicle.mileage;
        
        renderFuelChart(vehicle);
        
    } catch (error) {
        showToast('Error loading vehicle details', 'error');
    }
}

function renderFuelChart(vehicle) {
    const ctx = document.getElementById('fuelChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            datasets: [{
                label: 'Fuel Consumption (L)',
                data: [40, 55, 30, 45], // Mock data for V1
                borderColor: '#2563eb',
                backgroundColor: 'rgba(37, 99, 235, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            animation: {
                y: { duration: 2000, easing: 'easeOutQuart' }
            }
        }
    });
}
