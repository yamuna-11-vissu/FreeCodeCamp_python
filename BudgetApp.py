class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({
            "amount": amount,
            "description": description
        })

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({
                "amount": -amount,
                "description": description
            })
            return True
        return False

    def get_balance(self):
        balance = 0
        for item in self.ledger:
            balance += item["amount"]
        return balance

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        title = self.name.center(30, "*")
        result = title + "\n"

        for item in self.ledger:
            description = item["description"][:23]
            amount = f"{item['amount']:.2f}"
            result += f"{description:<23}{amount:>7}\n"

        result += f"Total: {self.get_balance():.2f}"

        return result


def create_spend_chart(categories):
    result = "Percentage spent by category\n"

    # Calculate total withdrawals
    total_spent = 0
    spent = []

    for category in categories:
        category_spent = 0

        for item in category.ledger:
            if item["amount"] < 0:
                category_spent += abs(item["amount"])

        spent.append(category_spent)
        total_spent += category_spent

    # Calculate percentages rounded down to nearest 10
    percentages = []

    for amount in spent:
        if total_spent == 0:
            percentage = 0
        else:
            percentage = int((amount / total_spent) * 100)
            percentage = (percentage // 10) * 10

        percentages.append(percentage)

    # Create bar chart
    for level in range(100, -1, -10):
        result += f"{level:>3}|"

        for percentage in percentages:
            if percentage >= level:
                result += " o "
            else:
                result += "   "

        result += " \n"

    # Horizontal line
    result += "    " + "-" * (len(categories) * 3 + 1) + "\n"

    # Find longest category name
    max_length = 0
    for category in categories:
        if len(category.name) > max_length:
            max_length = len(category.name)

    # Category names vertically
    for i in range(max_length):
        result += "     "

        for category in categories:
            if i < len(category.name):
                result += category.name[i] + "  "
            else:
                result += "   "

        if i < max_length - 1:
            result += "\n"

    return result