from os import name

from config import logger, load_data, save_data
from exceptions import AuthorizationError, InsufficientFundsError, AccountNotFoundError, InvalidTransferError, AuthenticationError, AccountDeletionError, InterestCalculationError
from models import CreateAccount, TransferRequest, Deposit, Withdraw, BalanceResponse, DeleteAccountRequest, TransactionHistory, InterestCalculation
class BankService:
    def __init__(self):
        self.data = load_data()  # Load data from JSON file

    def save(self):
        save_data(self.data)  # Save data to JSON file

    def create_account(self, account_data: CreateAccount):
        """
        Create a new account and save it in JSON storage.
        """
        name = account_data.owner_name
        account_number = str(account_data.account_number)
        initial_deposit = account_data.initial_deposit

        # Check for duplicate account number
        if account_number in self.data["accounts"]:
            logger.error(f"Account creation failed: Duplicate account number {account_number}")
            raise ValueError("Account number already exists")

        # Check for negative initial deposit
        if initial_deposit < 0:
            logger.error(f"Account creation failed: Negative initial deposit {initial_deposit}")
            raise ValueError("Initial deposit cannot be negative")

        # Add account to dictionary
        self.data["accounts"][account_number] = {
            "owner_name": name,
            "balance": initial_deposit
        }

        # Save to JSON
        self.save()

        logger.info(f"Account created successfully: {account_number} for {name}")
        return account_number
    def deposit(self, deposit_data: Deposit):
        """Deposit funds into an account and update JSON storage.
        """ 
        account_number = str(deposit_data.account_number)
        amount = deposit_data.amount

        # Check if account exists
        if account_number not in self.data["accounts"]:
            logger.error(f"Deposit failed: Account {account_number} not found")
            raise AccountNotFoundError("Account not found")

        # Check for negative deposit amount
        if amount <= 0:
            logger.error(f"Deposit failed: Invalid deposit amount {amount} for account {account_number}")
            raise ValueError("Deposit amount must be greater than zero")

        # Update balance
        self.data["accounts"][account_number]["balance"] += amount

        # Save to JSON
        self.save()

        new_balance = self.data["accounts"][account_number]["balance"]
        logger.info(f"Deposit successful: {amount} deposited to account {account_number}. New balance: {new_balance}")
        return new_balance
    def withdraw(self, withdraw_data: Withdraw):
        """Withdraw funds from an account and update JSON storage.
        """
        account_number = str(withdraw_data.account_number)
        amount = withdraw_data.amount

        # Check if account exists
        if account_number not in self.data["accounts"]:
            logger.error(f"Withdrawal failed: Account {account_number} not found")
            raise AccountNotFoundError("Account not found")

        # Check for negative withdrawal amount
        if amount <= 0:
            logger.error(f"Withdrawal failed: Invalid withdrawal amount {amount} for account {account_number}")
            raise ValueError("Withdrawal amount must be greater than zero")

        # Check for sufficient funds
        if self.data["accounts"][account_number]["balance"] < amount:
            logger.error(f"Withdrawal failed: Insufficient funds for account {account_number}. Attempted to withdraw {amount}, but balance is {self.data['accounts'][account_number]['balance']}")
            raise InsufficientFundsError("Insufficient funds")

        # Update balance
        self.data["accounts"][account_number]["balance"] -= amount

        # Save to JSON
        self.save()

        new_balance = self.data["accounts"][account_number]["balance"]
        logger.info(f"Withdrawal successful: {amount} withdrawn from account {account_number}. New balance: {new_balance}")
        return new_balance
    def get_balance(self, balance_request: BalanceResponse):
        """Get the balance of an account from JSON storage.
        """
        account_number = str(balance_request.account_number)

        # Check if account exists
        if account_number not in self.data["accounts"]:
            logger.error(f"Balance check failed: Account {account_number} not found")
            raise AccountNotFoundError("Account not found")

        balance = self.data["accounts"][account_number]["balance"]
        logger.info(f"Balance check successful: Account {account_number} has balance {balance}")
        return balance
    def transfer(self, transfer_data: TransferRequest):
        """Transfer funds between accounts and update JSON storage.
        """
        from_account_number = str(transfer_data.from_account_number)
        to_account_number = str(transfer_data.to_account_number)
        amount = transfer_data.amount

        # Check if both accounts exist
        if from_account_number not in self.data["accounts"]:
            logger.error(f"Transfer failed: Source account {from_account_number} not found")
            raise AccountNotFoundError("Source account not found")
        if to_account_number not in self.data["accounts"]:
            logger.error(f"Transfer failed: Destination account {to_account_number} not found")
            raise AccountNotFoundError("Destination account not found")

        # Check for negative transfer amount
        if amount <= 0:
            logger.error(f"Transfer failed: Invalid transfer amount {amount} from account {from_account_number} to account {to_account_number}")
            raise ValueError("Transfer amount must be greater than zero")

        # Check for sufficient funds in source account
        if self.data["accounts"][from_account_number]["balance"] < amount:
            logger.error(f"Transfer failed: Insufficient funds in source account {from_account_number}. Attempted to transfer {amount}, but balance is {self.data['accounts'][from_account_number]['balance']}")
            raise InsufficientFundsError("Insufficient funds in source account")

        # Perform transfer
        self.data["accounts"][from_account_number]["balance"] -= amount
        self.data["accounts"][to_account_number]["balance"] += amount

        # Save to JSON
        self.save()

        logger.info(f"Transfer successful: {amount} transferred from account {from_account_number} to account {to_account_number}")
        return True
    def delete_account(self, delete_request: DeleteAccountRequest):
        """Delete an account from JSON storage.
        """
        account_number = str(delete_request.account_number)

        # Check if account exists
        if account_number not in self.data["accounts"]:
            logger.error(f"Account deletion failed: Account {account_number} not found")
            raise AccountNotFoundError("Account not found")

        # Check if account has non-zero balance
        if self.data["accounts"][account_number]["balance"] > 0:
            logger.error(f"Account deletion failed: Account {account_number} has non-zero balance {self.data['accounts'][account_number]['balance']}")
            raise AccountDeletionError("Account cannot be deleted because it has a non-zero balance")

        # Delete account
        del self.data["accounts"][account_number]

        # Save to JSON
        self.save()

        logger.info(f"Account {account_number} deleted successfully")
        return True
    def get_transaction_history(self, account_number: int):
        """Get the transaction history of an account from JSON storage.
        """
        # Check if account exists
        if str(account_number) not in self.data["accounts"]:
            logger.error(f"Transaction history retrieval failed: Account {account_number} not found")
            raise AccountNotFoundError("Account not found")

        # For simplicity, we will return a placeholder transaction history
        transactions = [
            "Deposit: 100",
            "Withdrawal: 50",
            "Transfer to account 2: 20"
        ]

        logger.info(f"Transaction history retrieved successfully for account {account_number}")
        return transactions
    def calculate_interest(self, interest_calculation: InterestCalculation):
        """Calculate interest for an account based on the balance and interest rate.
        """
        account_number = str(interest_calculation.account_number)
        annual_rate = interest_calculation.annual_rate
        years = interest_calculation.years

        # Check if account exists
        if account_number not in self.data["accounts"]:
            logger.error(f"Interest calculation failed: Account {account_number} not found")
            raise AccountNotFoundError("Account not found")

        # Get current balance
        balance = self.data["accounts"][account_number]["balance"]

        # Calculate interest using simple interest formula: Interest = Principal * Rate * Time
        interest = balance * annual_rate * years

        logger.info(f"Interest calculated successfully for account {account_number}: {interest}")
        return interest