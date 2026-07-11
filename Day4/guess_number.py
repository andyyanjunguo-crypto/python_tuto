import random

target = random.randint(0, 100)
print("Welcome to the Guess the Number Game!")

number = -1
count = 0
while target != number: #need variable to count how many times user guessed
    count += 1
    number = int(input("Please enter a number between 0 and 100: "))
    if number < target:
        print("Your guess is too low.")
    elif number > target:
        print("Your guess is too high.")
    else:
        print("Congratulations! You guessed the correct number.")
#