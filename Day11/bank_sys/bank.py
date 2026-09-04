# ==========================
# 银行类（组合）
# ==========================
class Bank:

    def __init__(self, name):
        self.name = name
        self.accounts = {}

    # 开户
    def create_account(self, account):
        self.accounts[account.account_id] = account
        print(f"Account created for {account.owner}")

    # 查账户
    def find_account(self, account_id):
        return self.accounts.get(account_id)

    # 显示所有账户
    def list_accounts(self):
        print("\nAll Accounts")
        print("-" * 40)

        for acc in self.accounts.values():
            print(
                f"{acc.account_id} | {acc.owner} | "
                f"£{acc.balance:.2f} | {acc.__class__.__name__}"
            )

    # 银行统计
    @classmethod
    def welcome(cls):
        print("Welcome to Python Bank!")

    @staticmethod
    def validate_account_id(account_id):
        return account_id.startswith("ACC")
