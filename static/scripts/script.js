const input = document.getElementById("rating-input");
const stars = document.querySelectorAll(".stars .star");

// get gradient stops
const grad = document.querySelector("#starGradient");
const stops = grad.querySelectorAll("stop");

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
input.addEventListener("input", (e) => updateStars(e.target.value));

// initialize
updateStars(input.value);