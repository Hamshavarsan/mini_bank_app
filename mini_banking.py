from datetime import datetime

accounts = {}
next_account_number = 1001

def user_data():
    with open("user_data.txt", "w") as file:
        for acc_no, info in accounts.items():
            file.write(f"Account Number: {acc_no}\t")
            file.write(f"Holder: {info['name']}\t")
            file.write(f"Holder: {info['email']}\t")
            file.write(f"Holder: {info['phone']}\t")
            file.write(f"Balance: {info['balance']}\t")
            file.write("Transactions:\t")
            for transaction in info['transactions']:
                file.write(f"{transaction}\t")
            file.write("\n")


def create_account():
    global next_account_number

    name = input("Enter account holder name: ").strip()
    email= input("Enter account holder email:").strip()
    try:
        phone= int (input("Enter account holder phone number:").strip())
    except ValueError:
        print("Invalid phone number. Please enter phone number.")


    
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
        'email':email,
        'phone':phone,
        'balance': initial_balance,
        'transactions': [f"[{timestamp}] Initial deposit: {initial_balance}"]
    }
    print(f"Account created successfully! Your account number is {account_number}")
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



def admin_menu():
    while True:
        print("Admin Menu:")
        print("1. Create Account")
        print("2. View All Accounts")
        print("3. Logout")

        choice = input("Choose option (1-3): ").strip()
        if choice == '1':
            create_account()
        elif choice == '2':
            with open("user_data.txt","r") as file:
                print(file.read())   
        elif choice == '3':
            break
        else:
            print("Invalid choice.")



def  user_menu():
    acc_no = input("Enter your account number: ").strip()
    if acc_no in accounts:
        account_number=acc_no
        while True:
            print(f"Welcome {accounts[account_number]['name']}")
            print("1. Deposit Money")
            print("2. Withdraw Money")
            print("3. Check Balance")
            print("4. Transaction History")
            print("5. Logout")

            choice = input("Choose option (1-5): ").strip()
            if choice == '1':
                acc_no = input("Enter your account number: ").strip()
                if acc_no in accounts:
                    account_number=acc_no
                    deposit_money(account_number)
            elif choice == '2':
                acc_no = input("Enter your account number: ").strip()
                if acc_no in accounts:
                    account_number=acc_no
                    withdraw_money(account_number)
            elif choice == '3':
                acc_no = input("Enter your account number: ").strip()
                if acc_no in accounts:
                    account_number=acc_no
                    check_balance(account_number)
            elif choice == '4':
                acc_no = input("Enter your account number: ").strip()
                if acc_no in accounts:
                    account_number=acc_no
                    transaction_history(account_number)
            elif choice == '5':
                break
            
            
    else:
        print("Account not found.")
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
           user_menu()
        elif choice == '3':
            print("Thank you for using the banking app😊")
            break
        else:
            print("Invalid choice.")

login()






