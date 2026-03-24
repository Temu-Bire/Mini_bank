
# from .services import BankService
from services import BankService
from models import CreateAccount, Deposit, TransferRequest, Withdraw, BalanceResponse, DeleteAccountRequest, TransactionHistory, InterestCalculation
from exceptions import InsufficientFundsError, AccountNotFoundError, InvalidTransferError, AuthenticationError, AuthorizationError, AccountDeletionError, InterestCalculationError, TransactionHistoryError, AccountCreationError
from config import logger

bank_service = BankService()  # Initialize the bank service

def main():
   while True:
        print("\nMini Bank CLI")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transfer Funds")
        print("6. delete Account")
        print("7. Transaction History")
        print("8. Calculate Interest")
        print("9. Exit")
        choice = input("Enter your choice: ")

        match choice:
            case "1":
                name = input("Enter account owner name: ")
                account_number = int(input("Enter account number: "))
                initial_deposit = float(input("Enter initial deposit amount: "))
                account_data = CreateAccount(owner_name=name, account_number=account_number, initial_deposit=initial_deposit)
                try:
                    account_id = bank_service.create_account(account_data)
                    print(f"Account created successfully with ID: {account_id}")
                except ValueError as e:
                    print(f"Error creating account: {e}")
            case "2":
                account_number = int(input("Enter account number for deposit: "))
                amount = float(input("Enter deposit amount: "))
                deposit_data = Deposit(account_number=account_number, amount=amount)
                try:
                    new_balance = bank_service.deposit(deposit_data)
                    print(f"Deposit successful. New balance: {new_balance}")
                except (ValueError, AccountNotFoundError) as e:
                    print(f"Error during deposit: {e}")
            case "3":
                account_number = int(input("Enter account number for withdrawal: "))
                amount = float(input("Enter withdrawal amount: "))
                withdraw_data = Withdraw(account_number=account_number, amount=amount)
                try:
                    new_balance = bank_service.withdraw(withdraw_data)
                    print(f"Withdrawal successful. New balance: {new_balance}")
                except (ValueError, AccountNotFoundError, InsufficientFundsError) as e:
                    print(f"Error during withdrawal: {e}")
            case "4":
                account_number = int(input("Enter account number to check balance: "))
                balance_request = BalanceResponse(account_number=account_number, balance=0.0)  # Balance will be fetched in service
                try:
                    balance = bank_service.get_balance(balance_request)
                    print(f"Account number {account_number} has balance: {balance}")
                except AccountNotFoundError as e:
                    print(f"Error checking balance: {e}")
            case "5":
                from_account_number = int(input("Enter source account number for transfer: "))
                to_account_number = int(input("Enter destination account number for transfer: "))
                amount = float(input("Enter transfer amount: "))
                transfer_data = TransferRequest(from_account_number=from_account_number, to_account_number=to_account_number, amount=amount)
                try:
                    result = bank_service.transfer(transfer_data)
                    print(f"Transfer of {amount} successful.")
                except (ValueError, AccountNotFoundError, InsufficientFundsError) as e:
                    print(f"Error during transfer: {e}")
            case "6":
                account_number = int(input("Enter account number to delete: "))
                delete_request = DeleteAccountRequest(account_number=account_number)
                try:
                    bank_service.delete_account(delete_request)
                    print(f"Account {account_number} deleted successfully.")
                except (AccountNotFoundError, AccountDeletionError) as e:
                    print(f"Error deleting account: {e}")
            case "7":
                account_number = int(input("Enter account number to view transaction history: "))
                try:
                    history = bank_service.get_transaction_history(account_number)
                    print(f"Transaction history for account {account_number}:")
                    for transaction in history:
                        print(f"  - {transaction}")
                except TransactionHistoryError as e:
                    print(f"Error retrieving transaction history: {e}")
            case "8":
                account_number = int(input("Enter account number to calculate interest: "))
                interest_calculation = InterestCalculation(account_number=account_number, annual_rate=float('0.05'), years=1)  # Example values
                try:
                    interest = bank_service.calculate_interest(interest_calculation)
                    print(f"Calculated interest for account {account_number}: {interest}")
                except InterestCalculationError as e:
                    print(f"Error calculating interest: {e}")
            case "9":
                print("Exiting...")
                break
            case _:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()