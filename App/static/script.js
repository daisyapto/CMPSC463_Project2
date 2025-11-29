// script.js

const form = document.getElementById("evac-form");
const mapFrame = document.getElementById("map-frame");

const loader = document.getElementById("loader");
const progressBar = document.getElementById("load-bar");
const loaderText = document.querySelector(".loader-text");

// ------------------------
// Loader Utilities
// ------------------------

function updateProgress(pct) {
    progressBar.style.width = pct + "%";
}

function setText(text) {
    loaderText.innerText = text;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Fake pipeline loader
 * Matches backend execution flow
 */
async function simulateLoader() {

    loader.style.display = "flex";   // Show overlay

    setText("Loading GeoJSON Data...");
    updateProgress(15);
    await sleep(1000);

    setText("Building Road Graph...");
    updateProgress(35);
    await sleep(1000);

    setText("Running Dijkstra...");
    updateProgress(60);
    await sleep(1000);

    setText("Computing MST...");
    updateProgress(80);
    await sleep(700);

    setText("Rendering Map...");
    updateProgress(95);
    await sleep(5000);

    setText("Finishing Up...");
    updateProgress(95);
    await sleep(2000);

    updateProgress(100);
}

// ------------------------
// Form Handlers
// ------------------------

form.addEventListener("submit", async function (e) {
    e.preventDefault();

    const lat = document.getElementById("lat").value;
    const lon = document.getElementById("lon").value;
    const k = document.getElementById("k").value;

    // Start loader simulation
    simulateLoader();

    // Trigger map generation
    mapFrame.src = `/map?lat=${lat}&lon=${lon}&k=${k}`;
});

// ------------------------
// Hide loader when map finishes loading
// ------------------------

mapFrame.addEventListener("load", function () {
    loader.style.display = "none";
});
