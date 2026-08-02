document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch Profile for the Welcome Message
        const profile = await apiCall('/company/profile');
        const title = document.getElementById('welcome-title');
        title.innerHTML = `Welcome to <span>${profile.name}</span> Operations`;

        // Set Date Time
        const dtElement = document.getElementById('current-datetime');
        setInterval(() => {
            const now = new Date();
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
            dtElement.textContent = now.toLocaleDateString('en-IN', options);
        }, 1000);

        // Fetch Dashboard Metrics for the Checklist
        const metrics = await apiCall('/company/dashboard');
        
        // Checklist logic
        if (metrics.total_vehicles > 0) {
            const el = document.getElementById('check-vehicle');
            el.classList.add('completed');
            el.querySelector('i').classList.replace('fa-regular', 'fa-solid');
            el.querySelector('i').classList.replace('fa-circle', 'fa-circle-check');
            document.getElementById('check-vehicle-text').textContent = `You have registered ${metrics.total_vehicles} vehicles.`;
        }

        if (metrics.total_drivers > 0) {
            const el = document.getElementById('check-driver');
            el.classList.add('completed');
            el.querySelector('i').classList.replace('fa-regular', 'fa-solid');
            el.querySelector('i').classList.replace('fa-circle', 'fa-circle-check');
            document.getElementById('check-driver-text').textContent = `You have onboarded ${metrics.total_drivers} drivers.`;
        }

        if (metrics.total_orders > 0) {
            const el = document.getElementById('check-order');
            el.classList.add('completed');
            el.querySelector('i').classList.replace('fa-regular', 'fa-solid');
            el.querySelector('i').classList.replace('fa-circle', 'fa-circle-check');
            document.getElementById('check-order-text').textContent = `You have logged ${metrics.total_orders} orders.`;
        }
        
        if (metrics.completed_trips > 0) {
            const el = document.getElementById('check-trip');
            el.classList.add('completed');
            el.querySelector('i').classList.replace('fa-regular', 'fa-solid');
            el.querySelector('i').classList.replace('fa-circle', 'fa-circle-check');
            document.getElementById('check-trip-text').textContent = `You have successfully completed ${metrics.completed_trips} trips!`;
        }

    } catch (error) {
        console.error('Failed to load operations center', error);
    }
});
