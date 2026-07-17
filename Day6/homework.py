is_running = True
balance = 1000.0
transactions = 0
currency = "GBP"

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
        deposit_amount = int(input("Enter deposit amount: "))
        balance += deposit_amount
        transactions += 1  
        print(f"New balance: £{balance}")
        
    elif choice == "3":
        withdraw_amount = int(input("Enter withdrawal amount: "))
        
        if withdraw_amount > balance:
            print("Insufficient balance.")
        else:
            balance -= withdraw_amount
            transactions += 1  
            print(f"New balance: £{balance}")
            
    elif choice == "4":
        goodbye()
        is_running = False  
        
    else:
        print("Invalid option. Please try again.")