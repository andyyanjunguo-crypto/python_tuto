// console.log("Pokémon Trainer Lab started!");

// ------ Card1
let pokemonName = "Pikachu"
let id = "26"
let hp = 100
let initialAttact = 120
let attack = initialAttact
let defense = 60
let image = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"

function displayValues(newMessage) {
    nameElement.textContent = pokemonName;
    numberElement.textContent = "#"+id
    hpElement.textContent = hp
    attackElement.textContent = attack
    defenseElement.textContent = defense
    imgElement.src = image
    message.textContent = newMessage
}
// -------

const nameElement = document.querySelector("#pokemon-name");
const numberElement = document.querySelector("#pokemon-number");
const imgElement = document.querySelector("#pokemon-image");
const hpElement = document.querySelector("#hp");
const attackElement = document.querySelector("#attack");
const defenseElement = document.querySelector("#defense");
const initialMessage = document.querySelector("#message");

displayValues(initialMessage);

const powerUpButton = document.querySelector("#power-btn")
powerUpButton.addEventListener("click", () => {
    // random from 1-10
    attack += 5;
    defense += 5;
    hp += 5;

    displayValues("Pikachu Stat Increased!");
});


const takedamage = document.querySelector("#takedamage-btn");
takedamage.addEventListener("click", () => {
    attack -= 10;
    displayValues("Stats decreased!");
});

const resetButton = document.querySelector("#reset-btn");
resetButton.addEventListener("click", () => {
    attack = initialAttact;
    defense = 60;
    hp = 100;
    displayValues("Stats reset!");
});

const evolveButton = document.querySelector("#evolve-btn");
evolveButton.addEventListener("click", () => {
    pokemonName = "Raichu"
    id = "26"
    hp = 100
    attack = 120
    defense = 60
    image = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/26.png"
    displayValues("Pikachu has evolved into Raichu!")
})
