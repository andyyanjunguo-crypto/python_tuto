from account import Account

# ==========================
# 信用账户
# ==========================
class CreditAccount(Account):

    interest_rate = -0.10
    credit_limit = 500

    def withdraw(self, amount): # override parent's func

        available = self.balance + CreditAccount.credit_limit

        if amount > available:
            raise ValueError("Credit limit exceeded.")

        # 调用父类方法（余额够）
        if amount <= self.balance:
            super().withdraw(amount)

        else:
            remaining = amount - self.balance

            super().withdraw(self.balance)

            # 信用透支
            self._Account__balance -= remaining
            self.transactions.append(
                f"- Credit Used: £{remaining}"
            )

    def apply_interest(self):
        if self.balance < 0:
            debt_interest = abs(self.balance) * 0.10
            self._Account__balance -= debt_interest

            self.transactions.append(
                f"Credit interest charged: £{debt_interest:.2f}"
            )