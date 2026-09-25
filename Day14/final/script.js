// ========================================
// Pokémon Card
// Lesson 1: JavaScript DOM
// ========================================


// ----------------------------------------
// 1. Pokémon data
// ----------------------------------------

let pokemon = {

    name: "Pikachu",

    number: 25,

    level: 5,

    hp: 35,

    attack: 55,

    defense: 40,

    type: "⚡ Electric",

    image:
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"

};


// ----------------------------------------
// 2. Find HTML elements
// ----------------------------------------

const nameElement =
    document.querySelector("#pokemon-name");

const numberElement =
    document.querySelector("#pokemon-number");

const imageElement =
    document.querySelector("#pokemon-image");

const typeElement =
    document.querySelector("#pokemon-type");

const levelElement =
    document.querySelector("#level");

const hpElement =
    document.querySelector("#hp");

const attackElement =
    document.querySelector("#attack");

const defenseElement =
    document.querySelector("#defense");

const hpBar =
    document.querySelector("#hp-bar");

const attackBar =
    document.querySelector("#attack-bar");

const defenseBar =
    document.querySelector("#defense-bar");

const messageElement =
    document.querySelector("#message");


// ----------------------------------------
// 3. Find buttons
// ----------------------------------------

const powerButton =
    document.querySelector("#power-btn");

const damageButton =
    document.querySelector("#damage-btn");

const evolveButton =
    document.querySelector("#evolve-btn");

const resetButton =
    document.querySelector("#reset-btn");


// ----------------------------------------
// 4. Display Pokémon
// ----------------------------------------

function displayPokemon() {

    nameElement.textContent =
        pokemon.name;

    numberElement.textContent =
        "#" + pokemon.number;

    imageElement.src =
        pokemon.image;

    typeElement.textContent =
        pokemon.type;

    levelElement.textContent =
        pokemon.level;

    hpElement.textContent =
        pokemon.hp;

    attackElement.textContent =
        pokemon.attack;

    defenseElement.textContent =
        pokemon.defense;


    // Update stat bars

    hpBar.style.width =
        Math.min(pokemon.hp, 100) + "%";

    attackBar.style.width =
        Math.min(pokemon.attack, 100) + "%";

    defenseBar.style.width =
        Math.min(pokemon.defense, 100) + "%";
}


// ----------------------------------------
// 5. Power Up
// ----------------------------------------

function powerUp() {

    pokemon.level++;

    pokemon.hp += 5;

    pokemon.attack += 5;

    pokemon.defense += 3;


    messageElement.textContent =
        pokemon.name +
        " powered up! ⚡";


    displayPokemon();
}


// ----------------------------------------
// 6. Take Damage
// ----------------------------------------

function takeDamage() {

    const damage = 10;

    pokemon.hp -= damage;


    // HP cannot be below 0

    if (pokemon.hp < 0) {

        pokemon.hp = 0;

    }


    if (pokemon.hp === 0) {

        messageElement.textContent =
            pokemon.name +
            " fainted! 😵";

    } else {

        messageElement.textContent =
            pokemon.name +
            " took " +
            damage +
            " damage! 💥";

    }


    displayPokemon();
}


// ----------------------------------------
// 7. Evolve
// ----------------------------------------

function evolvePokemon() {

    pokemon.name = "Raichu";

    pokemon.number = 26;

    pokemon.hp = 60;

    pokemon.attack = 90;

    pokemon.defense = 55;

    pokemon.type = "⚡ Electric";

    pokemon.image =
        "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/26.png";


    messageElement.textContent =
        "✨ Pikachu evolved into Raichu!";


    displayPokemon();
}


// ----------------------------------------
// 8. Reset Pokémon
// ----------------------------------------

function resetPokemon() {

    pokemon = {

        name: "Pikachu",

        number: 25,

        level: 5,

        hp: 35,

        attack: 55,

        defense: 40,

        type: "⚡ Electric",

        image:
            "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"

    };


    messageElement.textContent =
        "Pikachu has been reset!";


    displayPokemon();
}


// ----------------------------------------
// 9. Button events
// ----------------------------------------

powerButton.addEventListener(
    "click",
    powerUp
);


damageButton.addEventListener(
    "click",
    takeDamage
);


evolveButton.addEventListener(
    "click",
    evolvePokemon
);


resetButton.addEventListener(
    "click",
    resetPokemon
);


// ----------------------------------------
// 10. Initial display
// ----------------------------------------

displayPokemon();