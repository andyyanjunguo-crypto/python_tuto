# Python Exercise: Simple ATM Simulator 💳

## Objective

Write a Python program that simulates a simple ATM.

## Requirements

1.  Create a variable called `balance` and set its value to **1000**.
2.  Repeatedly display the following menu:

``` text
1. Check Balance
2. Deposit Money
3. Withdraw Money
4. Exit
```

3.  Ask the user to choose an option.
4.  Use `if`, `elif`, and `else` statements to perform the selected
    action.

### Option 1 - Check Balance

Display the current balance.

### Option 2 - Deposit Money

-   Ask how much money to deposit.
-   Add the amount to the balance.
-   Display the updated balance.

### Option 3 - Withdraw Money

-   Ask how much money to withdraw.
-   If the amount is greater than the current balance, display:
    `Insufficient balance.`
-   Otherwise, subtract the amount and display the updated balance.

### Option 4 - Exit

Display: `Thank you for using the ATM.` Then end the program.

### Invalid Option

Display: `Invalid option. Please try again.`

### Additional Requirements

-   Keep showing the menu until the user chooses **Exit**.
-   Count how many transactions (deposit or withdrawal) the user
    performs.
-   When the user exits, display: `You completed X transaction(s).`

## Example Output

``` text
===== ATM MENU =====
1. Check Balance
2. Deposit Money
3. Withdraw Money
4. Exit

Choose an option: 2
Enter deposit amount: 300
New balance: £1300

Choose an option: 3
Enter withdrawal amount: 500
New balance: £800

Choose an option: 4
Thank you for using the ATM.
You completed 2 transaction(s).
```

## Python Knowledge Being Tested

-   Variables
-   `input()` and `print()`
-   `int()`
-   Arithmetic operators
-   Comparison operators
-   `if`, `elif`, `else`
-   `while` loops
-   Boolean variables
-   Counters
