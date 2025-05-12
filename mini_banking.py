import os
from datetime import datetime
import re


accounts = {}
next_account_number = 1001

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def user_data():
    with open("user_data.txt", "w") as file:
        for acc_no, info in accounts.items():
            file.write(f"Account Number: {acc_no}\t")
            file.write(f"Name: {info['name']}\t")
            file.write(f"Email: {info['email']}\t")
            file.write(f"Phone: {info['phone']}\t")
            file.write(f"Balance: {info['balance']}\t")
            file.write(f"Password: {info['password']}\t")
            file.write("Transactions:\t")
            for transaction in info['transactions']:
                file.write(f"{transaction}\t")
            file.write("\n")

def load_user_data():
    global next_account_number
    try:
        with open("user_data.txt", "r") as file:
            max_acc = 1000
            for line in file:
                parts = line.strip().split("\t")
                if len(parts) < 7:
                    continue
                acc_no = parts[0].split(": ")[1]
                name = parts[1].split(": ")[1]
                email = parts[2].split(": ")[1]
                phone = int(parts[3].split(": ")[1])
                balance = float(parts[4].split(": ")[1])
                password = parts[5].split(": ")[1]
                transactions_str = parts[6].replace("Transactions:\t", "")
                transactions = transactions_str.split("\t") if transactions_str else []
                accounts[acc_no] = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'balance': balance,
                    'password': password,
                    'transactions': transactions
                }
                max_acc = max(max_acc, int(acc_no))
            next_account_number = max_acc + 1
        print("User data loaded successfully.")
    except FileNotFoundError:
        print("No previous user data found.")


def create_account():
    global next_account_number
    name = input("Enter account holder name: ").strip()
    while True:
        email = input("Enter account holder email: ").strip()
        if is_valid_email(email):
            break
        else:
            print("Invalid email format. Please try again.")
    while True:
        try:
            phone = int(input("Enter account holder phone number: ").strip())
            break
        except ValueError:
            print("Invalid phone number. Please enter digits only.")
    while True:
        try:
            initial_balance = float(input("Enter initial balance: "))
            if initial_balance < 0:
                print("Initial balance cannot be negative.")
            else:
                break
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
    password = input("Set a password for your account: ").strip()
    account_number = str(next_account_number)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    accounts[account_number] = {
        'name': name,
        'email': email,
        'phone': phone,
        'balance': initial_balance,
        'password': password,
        'transactions': [f"[{timestamp}] Initial deposit: {initial_balance:.2f}"]
    }
    print(f"\nAccount created successfully! Your account number is {account_number}")
    next_account_number += 1
    user_data()

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
    accounts[account_number]['transactions'].append(f"[{timestamp}] Deposited: {amount:.2f}")
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
    accounts[account_number]['transactions'].append(f"[{timestamp}] Withdrew: {amount:.2f}")
    print("Withdrawal successful.")

def check_balance(account_number):
    print(f"Current balance: {accounts[account_number]['balance']:.2f}")

def transaction_history(account_number):
    print("Transaction History:")
    for transaction in accounts[account_number]['transactions']:
        print(f"- {transaction}")

def log_login(user_type, account_number=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("login_logs.txt", "a") as log_file:
        if user_type == "Admin":
            log_file.write(f"[{timestamp}] Admin logged in\n")
        elif user_type == "User":
            log_file.write(f"[{timestamp}] User logged in - Account No: {account_number}\n")

def admin_menu():
    while True:
        print("\n--- Admin Menu ---")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. Logout")
        choice = input("Choose option (1-4): ").strip()
        if choice == '1':
            create_account()
        elif choice == '2':
            try:
                with open("user_data.txt", "r") as file:
                    print("\n--- All Account Data ---")
                    print(file.read())
            except FileNotFoundError:
                print("No account data found.")
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

def user_menu():
    acc_no = input("Enter your account number: ").strip()
    if acc_no in accounts:
        password = input("Enter your password: ").strip()
        if password != accounts[acc_no]['password']:
            print("Incorrect password.")
            return
        log_login("User", acc_no)
        account_number = acc_no
        while True:
            print(f"\nWelcome {accounts[account_number]['name']}")
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
    else:
        print("Account not found.")

def login():
    while True:
        print("\n--- Login Menu ---")
        print("1. Admin Login")
        print("2. User Login")
        print("3. View Login Details")
        print("4. Exit")
        choice = input("Choose option (1-4): ").strip()
        if choice == '1':
            password = input("Enter admin password: ")
            if password == "admin123":
                log_login("Admin")
                admin_menu()
            else:
                print("Incorrect password.")
        elif choice == '2':
            user_menu()
        elif choice == '3':
            try:
                with open("login_logs.txt", "r") as file:
                    print("\n--- Login Logs ---")
                    print(file.read())
            except FileNotFoundError:
                print("No login records found.")
        elif choice == '4':
            print("Thank you for using the banking app 😊")
            break
        else:
            print("Invalid choice.")

load_user_data()
login()
