import datetime


class User:
    def __init__(self, user_id, pin, name):
        self.user_id = user_id
        self.pin = pin
        self.name = name
        self.account = Account()


class Account:
    def __init__(self):
        self.balance = 0
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            self.add_transaction("Withdrawal", amount)

    def transfer(self, target_account, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            target_account.balance += amount
            self.add_transaction("Transfer to " + target_account.owner.name, amount)

    def add_transaction(self, transaction_type, amount):
        timestamp = datetime.datetime.now()
        self.transaction_history.append({
            'type': transaction_type,
            'amount': amount,
            'timestamp': timestamp
        })


class ATM:
    @staticmethod
    def authenticate(user):
        user_id_input = input("Enter user ID: ")
        pin_input = input("Enter PIN: ")

        if user_id_input == user.user_id and pin_input == user.pin:
            return True
        else:
            print("Authentication failed. Incorrect user ID or PIN.")
            return False

    @staticmethod
    def display_menu():
        print("\nATM Menu:")
        print("1. Transactions History")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Transfer")
        print("5. Quit")

    @staticmethod
    def perform_transaction(user, option):
        if option == 1:
            ATM.display_transaction_history(user)
        elif option == 2:
            amount = float(input("Enter withdrawal amount: "))
            user.account.withdraw(amount)
        elif option == 3:
            amount = float(input("Enter deposit amount: "))
            user.account.deposit(amount)
        elif option == 4:
            target_user_id = input("Enter target user ID for transfer: ")
            target_user = find_user(target_user_id)
            if target_user:
                amount = float(input("Enter transfer amount: "))
                user.account.transfer(target_user.account, amount)
            else:
                print("Target user not found.")
        elif option == 5:
            print("Quitting...")
        else:
            print("Invalid option")

    @staticmethod
    def display_transaction_history(user):
        print("\nTransaction History:")
        for transaction in user.account.transaction_history:
            print(f"{transaction['timestamp']}: {transaction['type']} - ${transaction['amount']:.2f}")


def find_user(user_id):
    for user in users:
        if user.user_id == user_id:
            return user
    return None


# Sample Users
user1 = User("12345", "1234", "Alice")
user2 = User("67890", "5678", "Bob")

users = [user1, user2]

# Main Program
user_input = input("Welcome to the ATM system!\nPlease enter your user ID and PIN to proceed.\n")

authenticated_user = None
for user in users:
    if user_input == user.user_id:
        authenticated_user = user
        break

if authenticated_user and ATM.authenticate(authenticated_user):
    while True:
        ATM.display_menu()
        option = int(input("Select an option (1-5): "))
        if option == 5:
            break
        ATM.perform_transaction(authenticated_user, option)
else:
    print("Exiting program. Authentication failed.")
