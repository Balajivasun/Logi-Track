let allDrivers = [];

document.addEventListener('DOMContentLoaded', () => {
    loadDrivers();

    document.getElementById('driver-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            name: document.getElementById('drv-name').value,
            phone_number: document.getElementById('drv-phone').value,
            license_number: document.getElementById('drv-license').value,
            experience_years: parseInt(document.getElementById('drv-exp').value)
        };

        try {
            await apiCall('/drivers/', 'POST', payload);
            showToast('Driver onboarded successfully!', 'success');
            closeDriverModal();
            loadDrivers();
        } catch (error) {
            showToast(error.message, 'error');
        }
    });

    document.getElementById('driver-search').addEventListener('input', (e) => {
        renderDrivers(e.target.value.toLowerCase());
    });
});

async function loadDrivers() {
    try {
        allDrivers = await apiCall('/drivers/');
        renderDrivers();
    } catch (error) {
        showToast('Failed to load drivers', 'error');
    }
}

function getStatusBadge(status) {
    const clsMap = {
        'Available': 'status-available',
        'Assigned': 'status-assigned',
        'On Trip': 'status-ontrip',
        'Leave': 'status-leave'
    };
    const cssClass = clsMap[status] || 'status-leave';
    return `<span class="vehicle-status ${cssClass}">${status}</span>`;
}

function renderDrivers(searchQuery = '') {
    const grid = document.getElementById('driver-grid');
    grid.innerHTML = '';

    const filtered = allDrivers.filter(d => 
        d.name.toLowerCase().includes(searchQuery)
    );

    if (filtered.length === 0) {
        grid.innerHTML = `<div style="grid-column: 1/-1; text-align:center; padding: 3rem; color:var(--text-muted);">
            <i class="fa-solid fa-users" style="font-size:3rem; margin-bottom:1rem; opacity:0.5;"></i>
            <p>No drivers found.</p>
        </div>`;
        return;
    }

    filtered.forEach(driver => {
        const initials = driver.name.substring(0, 2).toUpperCase();
        const card = document.createElement('div');
        card.className = 'driver-card slide-up';
        
        card.innerHTML = `
            <div class="driver-header">
                <div class="driver-avatar">${initials}</div>
                <div style="flex:1;">
                    <h3>${driver.name}</h3>
                    <p><i class="fa-solid fa-phone" style="font-size:0.8rem; margin-right:0.3rem;"></i>${driver.phone_number}</p>
                </div>
            </div>
            
            <div class="driver-stats">
                <div><span>License</span><strong>${driver.license_number}</strong></div>
                <div><span>Experience</span><strong>${driver.experience_years} Years</strong></div>
            </div>
            
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.5rem;">
                ${getStatusBadge(driver.status)}
                <button class="btn-delete" onclick="deleteDriver(${driver.id}, '${driver.status}')"><i class="fa-solid fa-trash"></i></button>
            </div>
        `;
        grid.appendChild(card);
    });
}

async function deleteDriver(id, status) {
    if (status === 'On Trip' || status === 'Assigned') {
        showToast('Cannot delete a driver that is currently assigned to a trip.', 'error');
        return;
    }
    
    if (confirm('Are you sure you want to delete this driver?')) {
        try {
            await apiCall(`/drivers/${id}`, 'DELETE');
            showToast('Driver removed.', 'success');
            loadDrivers();
        } catch (error) {
            showToast(error.message, 'error');
        }
    }
}
