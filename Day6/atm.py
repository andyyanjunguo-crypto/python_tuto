is_running = True
balance = 1000.0
transactions = 0
currency = "GBP"

def withdraw_money(balance: float):
    withdraw_amount = float(input("Enter withdrawal amount: "))
        
    if withdraw_amount > balance:
        print("Insufficient balance.")
    else:
        balance -= withdraw_amount
        print(f"New balance: £{balance}")
    return balance

def deposit_money(balance: float):
    deposit_amount = float(input("Enter deposit amount: "))
    balance += deposit_amount
    return balance

def currency_symbol(currency: str):
    currency_symbol = "$"
    if currency == "GBP":
        currency_symbol = "£"
    elif currency == "RMB":
        currency_symbol = "¥"
    elif currency == "EUR":
        currency_symbol = "€"
    
    return currency_symbol

def check_balance(balance: float, currency: str = "GBP"):
    symbol = currency_symbol(currency)
    print(f"Current_balance: {symbol}{balance}")
    
def goodbye():
    print("Thank you for using the ATM.")
    print(f"You completed {transactions} transaction(s).")

def count_transcations(amount: float):
    if amount != balance:
        trasactions += 1

while is_running:
    print("ATM MENU")
    print("1. Check Balance")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Exit")
    
    #User's choice
    choice = input("Choose an option: ")
    
    if choice == "1":
        check_balance(balance, currency=currency)
        
    elif choice == "2":
        currency_balance = deposit_money(balance)
        count_transcations(currency_balance)
        balance = currency_balance
        print(f"New balance: £{balance}")
        
    elif choice == "3":
        currency_balance = withdraw_money(balance)
        count_transcations(currency_balance)
        balance = currency_balance
        print(f"New balance: £{balance}")
            
    elif choice == "4":
        goodbye()
        is_running = False  
        
    else:
        print("Invalid option. Please try again.")
