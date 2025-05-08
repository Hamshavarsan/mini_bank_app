from datetime import datetime


accounts = {}
next_account_number = 1001

def save_data_to_file():
    with open("bank_data.txt", "w") as file:
        for acc_no, info in accounts.items():
            file.write(f"Account Number: {acc_no}\t")
            file.write(f"Holder: {info['name']}\t")
            file.write(f"Balance: {info['balance']}\t")
            file.write("Transactions:\t")
            for transaction in info['transactions']:
                file.write(f"{transaction}\t")
            file.write("\n")
    

def create_account():
    global next_account_number

    name = input("Enter account holder name: ").strip()
    try:
        initial_balance = float(input("Enter initial balance: "))
        if initial_balance < 0:
            print("Initial balance cannot be negative.")
            return
    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
        return

    account_number = str(next_account_number)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    accounts[account_number] = {
        'name': name,
        'balance': initial_balance,
        'transactions': [f"[{timestamp}] Initial deposit: {initial_balance}"]
    }
    print(f"Account created successfully! Your account number is {account_number}")
    next_account_number += 1
    save_data_to_file()

def deposit_money(account_number):
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
    except ValueError:
        print("Invalid input.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    accounts[account_number]['balance'] += amount
    accounts[account_number]['transactions'].append(f"[{timestamp}] Deposited: {amount}")
    print("Deposit successful.")

def withdraw_money(account_number):
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
    except ValueError:
        print("Invalid input.")
        return

    if amount > accounts[account_number]['balance']:
        print("Insufficient funds.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    accounts[account_number]['balance'] -= amount
    accounts[account_number]['transactions'].append(f"[{timestamp}] Withdrew: {amount}")
    print("Withdrawal successful.")


def check_balance(account_number):
    print(f"Current balance: {accounts[account_number]['balance']}")


def transaction_history(account_number):
    print("Transaction History:")
    for transaction in accounts[account_number]['transactions']:
        print(f"- {transaction}")


def save_data_to_file():
    with open("bank_data.txt", "a") as file:
        for acc_no, info in accounts.items():
            file.write(f"Account Number: {acc_no}\t")
            file.write(f"Holder: {info['name']}\t")
            file.write(f"Balance: {info['balance']}\t")
            file.write("Transactions:\t")
            for transaction in info['transactions']:
                file.write(f"  {transaction}\t")
            file.write("\n")
    print("Data saved to 'bank_data.txt'")

def admin_menu():
    while True:
        print("Admin Menu:")
        print("1. Create Account")
        print("2. View All Accounts")
        #print("3. Save Data to File")
        print("3. Logout")

        choice = input("Choose option (1-3): ").strip()
        if choice == '1':
            create_account()
        elif choice == '2':
            for acc_no, info in accounts.items():
                print(f"\nAccount Number: {acc_no}")
                print(f"Holder: {info['name']}")
                print(f"Balance: {info['balance']}")
                print("Transactions:")
                for t in info['transactions']:
                    print(f"  {t}")
                # elif choice == '3':
                #     save_data_to_file()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")


def user_menu(account_number):
    while True:
        print(f"Welcome {accounts[account_number]['name']}")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Logout")

        choice = input("Choose option (1-5): ").strip()

        if choice == '1':
            deposit_money(account_number)
        elif choice == '2':
            withdraw_money(account_number)
        elif choice == '3':
            check_balance(account_number)
        elif choice == '4':
            transaction_history(account_number)
        elif choice == '5':
            break
        else:
            print("Invalid choice.")

def login():
    while True:
        print("Login Menu:")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")

        choice = input("Choose option (1-3): ").strip()

        if choice == '1':
            password = input("Enter admin password: ")
            if password == "admin123":
                admin_menu()
            else:
                print("Incorrect password.")
        elif choice == '2':
            acc_no = input("Enter your account number: ").strip()
            if acc_no in accounts:
                user_menu(acc_no)
            else:
                print("Account not found.")
        elif choice == '3':
            print("Thank you")
            break
        else:
            print("Invalid choice.")

login()


