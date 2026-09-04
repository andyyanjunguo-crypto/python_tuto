from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

# ==========================
# 抽象账户类
# ==========================
@dataclass
class Account(ABC):

    account_id: str
    owner: str
    __balance: float
    transactions: List[str] = field(default_factory=list)
    age: int = 0 

    # ---------- Property ----------
    @property
    def balance(self):
        return self.__balance

    # ---------- 存钱 ----------
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")

        self.__balance += amount
        self.transactions.append(f"+ Deposit: £{amount}")

    # ---------- 取钱 ----------
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be positive.")

        if amount > self.__balance:
            raise ValueError("Insufficient funds.")

        self.__balance -= amount
        self.transactions.append(f"- Withdraw: £{amount}")

    # ---------- 转账 ----------
    def transfer(self, target_account, amount):
        self.withdraw(amount)
        target_account.deposit(amount)

        self.transactions.append(
            f"Transfer to {target_account.owner}: £{amount}"
        )

        target_account.transactions.append(
            f"Received from {self.owner}: £{amount}"
        )

    # ---------- 查看账户 ----------
    def show_info(self):
        print("=" * 40)
        print(f"Account ID: {self.account_id}")
        print(f"Owner     : {self.owner}")
        print(f"Balance   : £{self.balance:.2f}")
        print(f"Type      : {self.__class__.__name__}")

    # ---------- 查看流水 ----------
    def show_transactions(self):
        print(f"\nTransaction History ({self.owner})")

        if not self.transactions:
            print("No transactions.")
            return

        for item in self.transactions:
            print(item)

    # ---------- 多态接口 ----------
    @abstractmethod
    def apply_interest(self):
        pass
