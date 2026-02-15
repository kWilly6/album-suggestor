const ratingInput = document.getElementById("rating-input");
const stars = document.querySelectorAll(".stars .star");
const reviewSubmit = document.getElementById("submit-button");
const userButton = document.getElementById("user-button");
const spotifySubmit = document.getElementById("spotify-submit")

// get gradient stops
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

function submitRating() {
    //check user
    //logic to add rating to database
    document.querySelector('.review-input').classList.add('hidden');
    document.querySelector('.reviews-display').classList.remove('hidden');
}

reviewSubmit.addEventListener("click", submitRating);

function resetReviewInputPanel() {
    document.querySelector('.reviews-display').classList.add('hidden');
    document.querySelector('.review-input').classList.remove('hidden');
}

userButton.addEventListener("click", resetReviewInputPanel);

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

spotifySubmit.addEventListener("click", fetchSpotifyData)