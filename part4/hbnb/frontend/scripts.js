document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }
});

const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';

async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();

            // Store JWT token
            document.cookie = `token=${data.access_token}; path=/`;

            // Redirect to index.html page
            window.location.href = 'index.html';
        } else {
            const errorData = await response.json();
            showError(errorData.message || 'Invalid email or password');
        }
    } catch (error) {
        showError('Unable to connect to server');
        console.error(error);
    }
}

function showError(message) {
    alert(`Login failed: ${message}`);
}
