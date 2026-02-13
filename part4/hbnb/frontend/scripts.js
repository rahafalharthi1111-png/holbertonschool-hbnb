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
	if (document.getElementById("places-list")) {
        fetchPlaces();
        setupPriceFilter();
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
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

function getCookie(name) {
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

/* Display Places */

let allPlaces = [];

function fetchPlaces(token) {
    fetch(`${API_BASE_URL}/places`, {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    })
        .then(response => response.json())
        .then(data => {
            allPlaces = data;
            displayPlaces(allPlaces);
        })
        .catch(error => console.error("Error fetching places:", error));
}

function displayPlaces(places) {
    const placesList = document.getElementById("places-list");
    placesList.innerHTML = "";

    places.forEach(place => {
        const placeCard = document.createElement("div");
        placeCard.classList.add("place-card");
        placeCard.setAttribute("data-price", place.price_by_night);

        placeCard.innerHTML = `
            <h2>${place.name}</h2>
            <p><strong>Price per night:</strong> $${place.price_by_night}</p>
            <p>${place.description}</p>
        `;

        placesList.appendChild(placeCard);
    });
}

/* Price Filter */

function setupPriceFilter() {
    const filter = document.getElementById("price-filter");

    if (!filter) return;

    filter.addEventListener("change", function () {
        const selectedPrice = this.value;
        const placeCards = document.querySelectorAll(".place-card");

        placeCards.forEach(card => {
            const price = parseInt(card.getAttribute("data-price"));

            if (selectedPrice === "all" || price <= parseInt(selectedPrice)) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    });
}
