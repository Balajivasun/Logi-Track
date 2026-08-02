let allOrders = [];

document.addEventListener('DOMContentLoaded', () => {
    loadOrders();

    document.getElementById('order-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const payload = {
            customer_name: document.getElementById('ord-customer').value,
            pickup_location: document.getElementById('ord-pickup').value,
            delivery_location: document.getElementById('ord-delivery').value,
            material: document.getElementById('ord-material').value,
            weight: parseFloat(document.getElementById('ord-weight').value),
            priority: document.getElementById('ord-priority').value,
            vehicle_id: parseInt(document.getElementById('ord-vehicle').value),
            driver_id: parseInt(document.getElementById('ord-driver').value)
        };

        try {
            await apiCall('/orders/', 'POST', payload);
            showToast('Order created and resources assigned!', 'success');
            closeOrderModal();
            loadOrders();
        } catch (error) {
            showToast(error.message, 'error');
        }
    });
    
    document.getElementById('status-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('status-order-id').value;
        const status = document.getElementById('status-select').value;
        
        try {
            await apiCall(`/orders/${id}/status`, 'PUT', { status: status });
            showToast('Order status updated.', 'success');
            closeStatusModal();
            loadOrders();
        } catch (error) {
            showToast(error.message, 'error');
        }
    });

    document.getElementById('order-search').addEventListener('input', (e) => {
        renderOrders(e.target.value.toLowerCase());
    });
});

async function loadOrders() {
    try {
        allOrders = await apiCall('/orders/');
        renderOrders();
    } catch (error) {
        showToast('Failed to load orders', 'error');
    }
}

async function openOrderModal() {
    try {
        // Fetch only available resources
        const vehicles = await apiCall('/vehicles/?status=Available');
        const drivers = await apiCall('/drivers/?status=Available');
        
        const vehSelect = document.getElementById('ord-vehicle');
        const drvSelect = document.getElementById('ord-driver');
        
        vehSelect.innerHTML = '';
        drvSelect.innerHTML = '';
        
        if (vehicles.length === 0) {
            vehSelect.innerHTML = '<option value="" disabled selected>No available vehicles</option>';
        } else {
            vehicles.forEach(v => {
                vehSelect.innerHTML += `<option value="${v.id}">${v.vehicle_number} (${v.type})</option>`;
            });
        }
        
        if (drivers.length === 0) {
            drvSelect.innerHTML = '<option value="" disabled selected>No available drivers</option>';
        } else {
            drivers.forEach(d => {
                drvSelect.innerHTML += `<option value="${d.id}">${d.name}</option>`;
            });
        }
        
        document.getElementById('order-modal').classList.remove('hidden');
    } catch (error) {
        showToast('Failed to load resources', 'error');
    }
}

function closeOrderModal() {
    document.getElementById('order-modal').classList.add('hidden');
    document.getElementById('order-form').reset();
}

function openStatusModal(id, currentStatus) {
    document.getElementById('status-order-id').value = id;
    document.getElementById('status-select').value = currentStatus;
    document.getElementById('status-modal').classList.remove('hidden');
}

function closeStatusModal() {
    document.getElementById('status-modal').classList.add('hidden');
}

// Close modals when clicking outside
document.addEventListener('click', (e) => {
    if (e.target.id === 'order-modal') {
        closeOrderModal();
    }
    if (e.target.id === 'status-modal') {
        closeStatusModal();
    }
});

function getStatusBadge(status) {
    const clsMap = {
        'Pending': 'status-pending',
        'Assigned': 'status-assigned',
        'Loading': 'status-loading',
        'In Transit': 'status-intransit',
        'Delivered': 'status-delivered',
        'Cancelled': 'status-pending'
    };
    const cssClass = clsMap[status] || 'status-pending';
    return `<span class="status-badge ${cssClass}">${status}</span>`;
}

function renderOrders(searchQuery = '') {
    const tbody = document.getElementById('order-table-body');
    tbody.innerHTML = '';

    const filtered = allOrders.filter(o => 
        o.customer_name.toLowerCase().includes(searchQuery)
    );

    if (filtered.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; color:var(--text-muted); padding:2rem;">No orders found.</td></tr>`;
        return;
    }

    filtered.forEach(order => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="order-id">#ORD-${order.id.toString().padStart(4, '0')}</td>
            <td>${order.customer_name}</td>
            <td>
                <div style="font-size:0.9rem;">
                    <div><i class="fa-solid fa-location-dot" style="color:var(--text-muted); width:15px;"></i> ${order.pickup_location}</div>
                    <div style="color:var(--text-muted); margin-left:5px;">|</div>
                    <div><i class="fa-solid fa-flag-checkered" style="color:var(--primary-color); width:15px;"></i> ${order.delivery_location}</div>
                </div>
            </td>
            <td>${order.material}<br><span style="font-size:0.8rem; color:var(--text-muted);">${order.weight} Tons</span></td>
            <td>${order.priority}</td>
            <td>${getStatusBadge(order.status)}</td>
            <td>
                <button class="action-btn" onclick="openStatusModal(${order.id}, '${order.status}')" ${order.status === 'Delivered' ? 'disabled' : ''}>
                    Update Status
                </button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}
