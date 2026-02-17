const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';


document.addEventListener('DOMContentLoaded', () => {

    //LOGIN PAGE
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            await loginUser(email, password);
        });
    }

    //INDEX PAGE
    if (document.getElementById('places-list')) {
        const token = getCookie('token');
        toggleLoginLink(token);
        if (token) fetchPlaces(token);
            loadPriceFilter();
    }

    //PLACE DETAILS PAGE
    if (document.querySelector('.place-info')) {
        initPlaceDetailsPage();
    }

    //ADD REVIEW PAGE
    if (document.getElementById('review-form') &&
        !document.querySelector('.place-info')) {
        initAddReviewPage();
    }
});



// LOGIN

async function loginUser(email, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
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
    alert(message);
}



// AUTH HELPERS

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value;
    }
    return null;
}

function toggleLoginLink(token) {
    const loginLink = document.getElementById('login-link');
    if (!loginLink) return;

    loginLink.style.display = token ? 'none' : 'block';
}



// INDEX PAGE

async function fetchPlaces(token) {
    try {
        const response = await fetch(`${API_BASE_URL}/places`, {
            method: 'GET',
            headers: { 'Authorization': `Bearer ${token}` }
        });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach(place => {
        const card = document.createElement('article');
        card.classList.add('place-card');
        card.setAttribute('data-price', place.price);




        
        card.innerHTML = `
            <h3>${place.title}</h3>
            <p>${place.description || ''}</p>
            <p><strong>Price:</strong> $${place.price} / night</p>
            <img src="/part4/hbnb/frontend/static/${place.image || 'place_default_001.jpg'}" alt="${place.title}" class="place-image">
            <a href="place.html?id=${place.id}" class="details-button">
                View Details
            </a>
        `;

        placesList.appendChild(card);
    });
}

function loadPriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) return;

    const options = [10, 50, 100, 'All'];

    options.forEach(option => {
        const opt = document.createElement('option');
        opt.value = option;
        opt.textContent = option;
        priceFilter.appendChild(opt);
    });

    priceFilter.addEventListener('change', filterPlacesByPrice);
}

function filterPlacesByPrice(event) {
    const selectedValue = event.target.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));
        card.style.display =
            (selectedValue === 'All' || price <= selectedValue)
                ? 'block'
                : 'none';
    });
}


function initPlaceDetailsPage() {
    const token = getCookie('token');
    const placeId = getPlaceIdFromURL();

    toggleLoginLink(token);

    const reviewSection = document.querySelector('.add-review');
    if (reviewSection) {
        reviewSection.style.display = token ? 'block' : 'none';
    }

    if (placeId) {
        fetchPlaceDetails(token, placeId);
        loadReviews(placeId);
    }

    // Add Review form submit
    const reviewForm = document.getElementById("review-form");
    if (reviewForm && token) {
        reviewForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById("review-text").value;
            const rating = document.getElementById("rating").value;

            try {
                const response = await fetch(`${API_BASE_URL}/reviews/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        text: reviewText,
                        rating: parseInt(rating),
                        place_id: placeId
                    })
                });

                if (!response.ok) throw new Error("Failed to add review");

                const newReview = await response.json();
                alert("Review added!");

                // Add new review to the DOM immediately
                appendReviewToDOM(newReview);
                reviewForm.reset();

            } catch (error) {
                alert("Error adding review");
                console.error(error);
            }
        });
    }
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const response = await fetch(`${API_BASE_URL}/places/${placeId}`, { headers });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

function displayPlaceDetails(place) {
    const placeInfo = document.querySelector('.place-info');
    if (!placeInfo) return;

    placeInfo.innerHTML = `
        <h1>${place.title}</h1>
        <p><strong>Price:</strong> $${place.price} / night</p>
        <p><strong>Description:</strong> ${place.description || ''}</p>
    `;

    // Amenities
    if (place.amenities?.length) {
        const title = document.createElement('h3');
        title.textContent = 'Amenities';
        const ul = document.createElement('ul');

        place.amenities.forEach(a => {
            const li = document.createElement('li');
            li.textContent = a.name || a;
            ul.appendChild(li);
        });

        placeInfo.appendChild(title);
        placeInfo.appendChild(ul);
    }
}

// LOAD REVIEWS
async function loadReviews(placeId) {
    const container = document.getElementById("reviews");
    if (!container) return;

    // Remove previous reviews except the <h2>
    container.querySelectorAll('.review-card').forEach(r => r.remove());

    try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`);
        if (!response.ok) {
            container.innerHTML += "<p>No reviews available.</p>";
            return;
        }

        const reviews = await response.json();
        if (reviews.length === 0) {
            container.innerHTML += "<p>No reviews yet.</p>";
            return;
        }

        reviews.forEach(review => appendReviewToDOM(review));

    } catch (error) {
        container.innerHTML += "<p>Error loading reviews.</p>";
        console.error(error);
    }
}

function appendReviewToDOM(review) {
    const container = document.getElementById("reviews");
    if (!container) return;

    const card = document.createElement("article");
    card.classList.add("review-card");

    card.innerHTML = `
        <p>${review.text}</p>
        <p>By: ${review.user_name || 'User'}</p>
        <p>${'⭐'.repeat(review.rating)}</p>
    `;

    container.appendChild(card);
}
