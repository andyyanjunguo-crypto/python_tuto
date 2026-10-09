// ========================================
// Pokémon Card
// Lesson 2: fetch() real data from our Python API
// ========================================


// ----------------------------------------
// 1. API address
//    Day14: data was written in the code
//    Day15: data comes from our FastAPI server
// ----------------------------------------

const API_BASE = "http://127.0.0.1:8000";


// ----------------------------------------
// 2. Type colors & emoji
// ----------------------------------------

const TYPE_STYLES = {
    normal:   { emoji: "⚪", color: "#dcdcc6" },
    fire:     { emoji: "🔥", color: "#ffb38a" },
    water:    { emoji: "💧", color: "#9dc3ff" },
    electric: { emoji: "⚡", color: "#ffd84d" },
    grass:    { emoji: "🌿", color: "#a7e08a" },
    ice:      { emoji: "❄️", color: "#b8f1f1" },
    fighting: { emoji: "🥊", color: "#e8908a" },
    poison:   { emoji: "☠️", color: "#d6a3e0" },
    ground:   { emoji: "⛰️", color: "#ecd59a" },
    flying:   { emoji: "🪽", color: "#c9b8ff" },
    psychic:  { emoji: "🔮", color: "#ffa3c2" },
    bug:      { emoji: "🐛", color: "#cde07a" },
    rock:     { emoji: "🪨", color: "#d9c77a" },
    ghost:    { emoji: "👻", color: "#b3a3d6" },
    dragon:   { emoji: "🐉", color: "#a99bff" },
    dark:     { emoji: "🌑", color: "#b8a596" },
    steel:    { emoji: "⚙️", color: "#cfcfe0" },
    fairy:    { emoji: "🧚", color: "#f5bfe0" },
};


// ----------------------------------------
// 3. Find HTML elements
// ----------------------------------------

const form = document.querySelector("#search-form");
const input = document.querySelector("#search-input");
const randomButton = document.querySelector("#random-btn");
const searchButton = document.querySelector("#search-btn");

const nameElement = document.querySelector("#pokemon-name");
const numberElement = document.querySelector("#pokemon-number");
const imageElement = document.querySelector("#pokemon-image");
const typesElement = document.querySelector("#pokemon-types");
const heightElement = document.querySelector("#height");
const weightElement = document.querySelector("#weight");
const messageElement = document.querySelector("#message");
const logElement = document.querySelector("#request-log");


// ----------------------------------------
// 4. Call our API with fetch()
//    async / await works just like in Python!
// ----------------------------------------

async function loadPokemon(nameOrId) {

    const url = API_BASE + "/pokemon/" + encodeURIComponent(nameOrId);
    const start = performance.now();

    showMessage("Loading...");
    setButtonsDisabled(true);

    try {

        const response = await fetch(url);
        const data = await response.json();

        const ms = Math.round(performance.now() - start);
        logElement.textContent = "GET " + url + " → " + response.status + " (" + ms + " ms)";

        if (!response.ok) {
            // FastAPI puts the error message in "detail"
            showMessage("😵 " + formatDetail(data.detail), true);
            return;
        }

        displayPokemon(data);
        showMessage(data.name + " is ready! (total power " + data.total + ")");

    } catch (error) {

        // fetch() itself failed: server not running, or CORS blocked
        logElement.textContent = "GET " + url + " → failed";
        showMessage("🔌 Cannot reach the API. Is uvicorn running?", true);

    } finally {

        setButtonsDisabled(false);

    }
}


// ----------------------------------------
// 5. Display Pokémon
// ----------------------------------------

function displayPokemon(pokemon) {

    nameElement.textContent = pokemon.name;
    numberElement.textContent = "#" + String(pokemon.id).padStart(3, "0");

    imageElement.src = pokemon.image || "";
    imageElement.alt = pokemon.name;

    heightElement.textContent = pokemon.height_m;
    weightElement.textContent = pokemon.weight_kg;

    // Type badges
    typesElement.replaceChildren();  // remove old badges
    for (const type of pokemon.types) {
        const style = TYPE_STYLES[type] || { emoji: "❓", color: "#ddd" };
        const badge = document.createElement("span");
        badge.className = "type-badge";
        badge.style.backgroundColor = style.color;
        badge.textContent = style.emoji + " " + type;
        typesElement.appendChild(badge);
    }

    // Stats (base stats go up to ~255, 150 fills the bar)
    for (const stat of ["hp", "attack", "defense", "speed"]) {
        const value = pokemon.stats[stat];
        document.querySelector("#" + stat).textContent = value;
        document.querySelector("#" + stat + "-bar").style.width =
            Math.min(value / 150 * 100, 100) + "%";
    }
}


// ----------------------------------------
// 6. Helpers
// ----------------------------------------

function showMessage(text, isError = false) {
    messageElement.textContent = text;
    messageElement.classList.toggle("error", isError);
}

function setButtonsDisabled(disabled) {
    searchButton.disabled = disabled;
    randomButton.disabled = disabled;
}

// 422 errors have a list in "detail", other errors have a string
function formatDetail(detail) {
    if (Array.isArray(detail)) {
        return detail.map((d) => d.msg).join(", ");
    }
    return detail;
}


// ----------------------------------------
// 7. Events
// ----------------------------------------

form.addEventListener("submit", (event) => {
    event.preventDefault();  // don't reload the page
    const name = input.value.trim();
    if (name) {
        loadPokemon(name);
    }
});

randomButton.addEventListener("click", () => {
    const id = Math.floor(Math.random() * 1025) + 1;
    input.value = id;
    loadPokemon(id);
});


// ----------------------------------------
// 8. Initial display
// ----------------------------------------

loadPokemon("pikachu");
