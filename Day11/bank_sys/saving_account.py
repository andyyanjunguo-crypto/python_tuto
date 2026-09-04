from account import Account

# ==========================
# 储蓄账户
# ==========================
class SavingsAccount(Account):

    interest_rate = 0.03

    def apply_interest(self):
        interest = self.balance * SavingsAccount.interest_rate
        self.deposit(interest)

        self.transactions.append(
            f"Interest added: £{interest:.2f}"
        )
