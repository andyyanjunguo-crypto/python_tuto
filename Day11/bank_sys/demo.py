from bank import Bank
from saving_account import SavingsAccount
from credit_account import CreditAccount
import json

# ==========================
# 主程序
# ==========================
def start():

    Bank.welcome()

    bank = Bank("Python Bank")

    alice = SavingsAccount("ACC1001", "Alice", 1000)
    bob = SavingsAccount("ACC1002", "Bob", 500)
    charlie = CreditAccount("ACC2001", "Charlie", 100)

    bank.create_account(alice)
    bank.create_account(bob)
    bank.create_account(charlie)

    # 存钱
    alice.deposit(200)

    # 取钱
    bob.withdraw(100)

    # 转账
    alice.transfer(bob, 150)

    # 信用账户透支
    charlie.withdraw(400)

    # 利息
    alice.apply_interest()
    charlie.apply_interest()

    # 显示账户
    bank.list_accounts()

    print("\n")
    alice.show_info()
    alice.show_transactions()

    print("\n")
    charlie.show_info()
    charlie.show_transactions()


if __name__ == "__main__":
    start()