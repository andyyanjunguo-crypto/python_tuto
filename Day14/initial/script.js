// console.log("Pokémon Trainer Lab started!");

// ------ Card1
let pokemonName = "Raichu"
let id = "26"
let hp = 100
let initialAttact = 120
let attack = initialAttact
let defense = 60
let image = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/26.png"

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

    displayValues("Pikachu power up!");
});

// resetButton.addEventListener("click", () => {
//     attack = initialAttact
//     attackElement.textContent = attack;
// });
