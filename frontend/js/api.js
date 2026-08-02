const API_URL = window.location.origin.includes('localhost') ? 'http://localhost:8000/api' : window.location.origin + '/api';

// Base API handler
async function apiCall(endpoint, method = 'GET', body = null, requireAuth = true) {
    const headers = {
        'Content-Type': 'application/json',
    };

    if (requireAuth) {
        const companyId = localStorage.getItem('company_id');
        if (!companyId) {
            window.location.href = '/index.html';
            return;
        }
        headers['Company-ID'] = companyId;
    }

    const config = {
        method,
        headers,
    };

    if (body) {
        config.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${API_URL}${endpoint}`, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Something went wrong');
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-circle';
    if (type === 'warning') icon = 'fa-exclamation-triangle';
    
    toast.innerHTML = `<i class="fa-solid ${icon}"></i> <span>${message}</span>`;
    
    container.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease-out reverse forwards';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}
