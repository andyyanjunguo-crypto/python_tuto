# Python Exercise: Guess the Random Number 🎯

## Objective

Write a Python program that lets the user guess a randomly generated
number.

## Requirements

Complete the Python program so that it behaves as follows:

1.  Import the `random` module.
2.  Generate a random integer between **0 and 100** (inclusive). This is
    the **target number**.
3.  Ask the user to enter a number.
4.  Compare the user's guess with the target number.
5.  Display one of the following messages:
    -   If the guess is **greater than** the target number:

            Number too large

    -   If the guess is **less than** the target number:

            Number too small

    -   If the guess is **equal to** the target number:

            Correct!
6.  Continue asking the user to guess until they enter the correct
    number.
7.  Count how many guesses the user makes.
8.  When the user guesses correctly, display the total number of
    guesses.

## Starter Code

``` python
# Import the random module
_____

# Generate a random number between 0 and 100
target = _____

# Count the number of guesses
count = 0

# Keep asking until the user guesses correctly
while _____:
    guess = int(input("Enter a number (0-100): "))
    count += 1

    if guess > target:
        print("Number too large")
    elif guess < target:
        print("Number too small")
    else:
        print("Correct!")
        print("You guessed the number in", count, "attempt(s).")
```

## Example Output

``` text
Enter a number (0-100): 75
Number too large

Enter a number (0-100): 20
Number too small

Enter a number (0-100): 50
Number too small

Enter a number (0-100): 63
Correct!
You guessed the number in 4 attempt(s).
```

## Bonus Challenge

-   Limit the player to **10 guesses**.
-   Give a hint such as **"Very close!"** if the guess is within 5 of
    the target.
-   Ask the user if they want to **play again** after finishing.
-   Validate the input so the user can only enter numbers between **0
    and 100**.
