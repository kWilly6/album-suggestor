const spotifySubmit = document.getElementById("spotify-submit");

// ──────────────────────────────
// USER LOGIC
// ──────────────────────────────
const loginButton = document.getElementById("login-button");
const userList = document.getElementById('userList');
const userID_input = document.getElementById('username');

let users = [];
let currentUser = null;

function updateLoginMenu() {
    if (currentUser) {
        loginButton.textContent = currentUser.username;
        loginButton.classList.add('logged-in');
    } else {
        loginButton.textContent = 'LOGIN';
        loginButton.classList.remove('logged-in');
    }
}

function toggleDropdown() {
    dropdownMenu.classList.toggle('show');
}

function closeDropdown() {
    dropdownMenu.classList.remove('show');
}

async function addNewUser() {
    const usernameInput = prompt("Enter new username:");
    if (!usernameInput || usernameInput.trim() === "") return;

    const username = usernameInput.trim();

    try {
        const response = await fetch('/add_new_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username: username })
        });

        const result = await response.json();

        if (result.success) {
            // Add to the dropdown list immediately            
            const li = document.createElement('li');
            li.className = 'user-item';
            li.textContent = result.username;
            li.onclick = () => selectUser(result.username);   // reuse your selectUser function
            userList.prepend(li);  // add to top

            // Automatically select the new user
            selectUser(result.username);
        } else {
            alert(result.error || "Failed to add user");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Error connecting to server");
    }
}

function selectUser(username) {
    currentUser = { username: username };
    // Update button text and style
    loginButton.textContent = username;
    loginButton.classList.add('logged-in');
    // Save to localStorage
    localStorage.setItem('currentUser', JSON.stringify(currentUser));
    userID_input.value = currentUser.username;
    console.log('User set');
    // Close dropdown
    dropdownMenu.classList.remove('show');
}

function attachUserClickListeners() {
    const userItems = userList.querySelectorAll('.user-item');

    userItems.forEach(item => {
        item.addEventListener('click', () => {
            const username = item.textContent.trim();
            selectUser(username);
        });
    });
}

// Event Listeners

//Extend Dropdown
loginButton.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleDropdown();
});

//Add New User Button
newUserOption.addEventListener('click', (e) => {
    e.stopPropagation();
    addNewUser();
});

// Close dropdown when clicking outside
document.addEventListener('click', () => {
    closeDropdown();
});

//Close dropdown
dropdownMenu.addEventListener('click', (e) => {
    e.stopPropagation();
});

// Page load user if any
function initLogin() {
    // Load previously selected user from localStorage
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            // Only restore if the user still exists in the current list
            const userExists = Array.from(userList.children).some(
                li => li.textContent.trim() === currentUser.username
            );
            if (userExists) {
                loginButton.textContent = currentUser.username;
                loginButton.classList.add('logged-in');
                userID_input.value = currentUser.username
                console.log('User set');
            }
        } catch (e) {
            console.error("Failed to parse saved user");
            loginButton.textContent = 'USER';
            loginButton.classList.remove('logged-in');
            userID_input.value = 'USER';
            currentUser.username = 'USER'
            console.log('User cleared Exception');
        }
    }
    else {
        console.error("Failed to parse saved user");
        loginButton.textContent = 'USER';
        loginButton.classList.remove('logged-in');
        userID_input.value = 'USER';
        currentUser.username = 'USER'
        console.log('User cleared Else');
    }

    // Make sure clicking on existing <li> elements works
    userList.querySelectorAll('.user-item').forEach(item => {
        item.addEventListener('click', () => {
            const username = item.getAttribute('data-username') || item.textContent.trim();
            selectUser(username);
        });
    });
}

// Run when page loads
document.addEventListener('DOMContentLoaded', initLogin);


// ──────────────────────────────
// RATING SUBMISSION LOGIC
// ──────────────────────────────
const ratingInput = document.getElementById("rating-input");
const stars = document.querySelectorAll(".stars .star");
const reviewSubmit = document.getElementById("submit-button");
const reviewForm = document.getElementById("review-form");
const reviewTextArea = document.getElementById("review_text");
const starGradFill = document.querySelector("#starGradient");
const stops = starGradFill.querySelectorAll("stop");

function updateStars(value) {
    const rating = Math.max(0, Math.min(10, parseFloat(value) || 0));

    stars.forEach((star, i) => {
        const index = i + 1;
        star.classList.remove("filled", "partial");

        if (rating >= index) {
            // Full star
            star.classList.add("filled");
        } else if (rating > index - 1 && rating < index) {
            // Fractional star
            const fraction = rating - (index - 1); // 0..1
            star.classList.add("partial");

            // Update gradient split point
            stops[0].setAttribute("offset", `${fraction * 100}%`);
            stops[1].setAttribute("offset", `${fraction * 100}%`);
        }
    });
}
// hook to input
ratingInput.addEventListener("input", (e) => updateStars(e.target.value));

function submitReview(event) {

    console.log('📤 Submit event triggered - starting validation...');
    let isValid = true;
    let errors = [];

    // Clear previous errors
    document.querySelectorAll('.error-message').forEach(el => el.remove());

    // Validate Rating
    const rating = parseFloat(ratingInput.value);
    if (!ratingInput.value || isNaN(rating) || rating < 0 || rating > 10) {
        isValid = false;
        errors.push("Rating must be between 0.0 and 10.0");
        ratingInput.classList.add('error');
    } else {
        ratingInput.classList.remove('error');
    }

    // Validate Review Text
    if (!reviewTextArea.value.trim()) {
        isValid = false;
        errors.push("Please write a review");
        reviewTextArea.classList.add('error');
    } else {
        reviewTextArea.classList.remove('error');
    }

    if (!isValid) {
        event.preventDefault();           // Stop form from submitting
        showErrors(errors);
        return false;
    }

    // Optional: Disable button to prevent double submission
    const submitBtn = document.getElementById('submit-button');
    submitBtn.disabled = true;
    submitBtn.textContent = "Submitting...";

    //logic to add rating to database
    document.querySelector('.review-input').classList.add('hidden');
    document.querySelector('.reviews-display').classList.remove('hidden');
}

reviewForm.addEventListener("submit", submitReview);

function showErrors(errors) {
    const container = document.querySelector('.rating').parentElement;
    errors.forEach(error => {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.style.color = 'red';
        errorDiv.style.fontSize = '0.9em';
        errorDiv.style.marginTop = '5px';
        errorDiv.textContent = error;
        container.appendChild(errorDiv);
    });
}

// function resetReviewInputPanel() {
//     document.querySelector('.reviews-display').classList.add('hidden');
//     document.querySelector('.review-input').classList.remove('hidden');
// }

// loginButton.addEventListener("click", resetReviewInputPanel);

// initialize
updateStars(ratingInput.value);

async function fetchSpotifyData() {
    const urlInput = document.getElementById('spotify-url').value;

    const response = await fetch('/get_album_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: urlInput })
    });

    if (response.ok) {
        const data = await response.json();
        updateUI(data);
    } else {
        alert("Could not find album data.");
    }
}

function updateUI(data) {
    document.getElementById('album-title').innerText = data.title;
    document.getElementById('album-artist').innerText = data.artist;
    document.getElementById('album-cover').src = data.cover_art;
    document.getElementById('album-year').innerText = data.year;
    document.getElementById('album-num-songs').innerText = data.num_songs;
    document.getElementById('album-duration').innerText = data.duration;
}

spotifySubmit.addEventListener("click", fetchSpotifyData);