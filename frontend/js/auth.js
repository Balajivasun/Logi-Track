function toggleAuth() {
    document.getElementById('login-box').classList.toggle('hidden');
    document.getElementById('register-box').classList.toggle('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;

            try {
                const response = await fetch(API_URL + '/auth/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        email: email,
                        password: password
                    })
                });

                const data = await response.json();
                if (!response.ok) throw new Error(data.detail || 'Login failed');

                localStorage.setItem('company_id', data.company_id);
                window.location.href = '/operations.html';
            } catch (error) {
                alert(error.message);
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const name = document.getElementById('reg-company-name').value;
            const email = document.getElementById('reg-email').value;
            const phone = document.getElementById('reg-phone').value;
            const password = document.getElementById('reg-password').value;

            try {
                const response = await fetch(API_URL + '/auth/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: name,
                        email: email,
                        password: password,
                        contact_number: phone
                    })
                });

                const data = await response.json();
                if (!response.ok) throw new Error(data.detail || 'Registration failed');

                alert('Registration successful! You can now login.');
                toggleAuth();
            } catch (error) {
                alert(error.message);
            }
        });
    }
});
