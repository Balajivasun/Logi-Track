document.addEventListener('DOMContentLoaded', async () => {
    try {
        const metrics = await apiCall('/company/dashboard');
        
        document.getElementById('total-vehicles').textContent = metrics.total_vehicles;
        document.getElementById('vehicles-ontrip').textContent = metrics.vehicles_on_trip;
        document.getElementById('total-drivers').textContent = metrics.total_drivers;
        document.getElementById('active-orders').textContent = metrics.active_orders;
        document.getElementById('completed-trips').textContent = metrics.completed_trips;

    } catch (error) {
        console.error('Failed to load dashboard metrics', error);
    }
});
