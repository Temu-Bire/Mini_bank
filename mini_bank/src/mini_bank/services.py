from os import name

from config import logger
from exceptions import AuthorizationError, InsufficientFundsError, AccountNotFoundError, InvalidTransferError, AuthenticationError, AccountDeletionError, InterestCalculationError
from models import CreateAccount, TransferRequest, Deposit, Withdraw, BalanceResponse, DeleteAccountRequest, TransactionHistory, InterestCalculation
class BankService:
    def __init__(self, db):
        self.db = db
    def create_account(self, account_data: CreateAccount):
        # Implementation logic to create account
        name = account_data.owner_name
        account_number = account_data.account_number
        initial_deposit = account_data.initial_deposit
        # Check for duplicate account number
        if self.db.get_account_by_number(account_number):
            logger.error(f"Account creation failed: Duplicate account number {account_number}")
            raise ValueError("Account number already exists")
        if initial_deposit < 0:
            logger.error(f"Account creation failed: Negative initial deposit {initial_deposit}")
            raise ValueError("Initial deposit cannot be negative")
        account_id = self.db.create_account(name, account_number, initial_deposit)
        logger.info(f"Account created successfully: {account_id} for {name}")
        return account_id
    def deposit(self,deposit_data: Deposit):
        # Implementation logic to deposit money
        account_id = deposit_data.account_id
        amount = deposit_data.amount
        if amount <= 0:
            logger.error(f"Deposit failed: Invalid amount {amount} for account {account_id}")
            raise ValueError("Deposit amount must be greater than zero")
        account = self.db.get_account(account_id)
        if not account:
            logger.error(f"Deposit failed: Account {account_id} not found")
            raise AccountNotFoundError("Account not found")
        new_balance = account.balance + amount
        self.db.update_balance(account_id, new_balance)
        logger.info(f"Deposit successful: {amount} deposited to account {account_id}. New balance: {new_balance}")
        return new_balance
    def withdraw(self, withdraw_data: Withdraw):
        # Implementation logic to withdraw money
        account_id = withdraw_data.account_id
        amount = withdraw_data.amount
        if amount <= 0:
            logger.error(f"Withdrawal failed: Invalid amount {amount} for account {account_id}")
            raise ValueError("Withdrawal amount must be greater than zero")
        account = self.db.get_account(account_id)
        if not account:
            logger.error(f"Withdrawal failed: Account {account_id} not found")
            raise AccountNotFoundError("Account not found")
        if account.balance < amount:
            logger.error(f"Withdrawal failed: Insufficient funds in account {account_id}. Available balance: {account.balance}, requested: {amount}")
            raise InsufficientFundsError("Insufficient funds")
        new_balance = account.balance - amount
        self.db.update_balance(account_id, new_balance)
        logger.info(f"Withdrawal successful: {amount} withdrawn from account {account_id}. New balance: {new_balance}")
        return new_balance
    def get_balance(self, balance_request: BalanceResponse):
        # Implementation logic to get account balance
        account_id = balance_request.account_id
        account = self.db.get_account(account_id)
        if not account:
            logger.error(f"Balance inquiry failed: Account {account_id} not found")
            raise AccountNotFoundError("Account not found")
        logger.info(f"Balance inquiry successful: Account {account_id} has balance {account.balance}")
        return account.balance
    def transfer(self, transfer_data: TransferRequest):
        # Implementation logic to transfer money between accounts
        from_account_id = transfer_data.from_account_id
        to_account_id = transfer_data.to_account_id
        amount = transfer_data.amount
        if amount <= 0:
            logger.error(f"Transfer failed: Invalid amount {amount} for transfer from account {from_account_id} to account {to_account_id}")
            raise ValueError("Transfer amount must be greater than zero")
        from_account = self.db.get_account(from_account_id)
        to_account = self.db.get_account(to_account_id)
        if not from_account:
            logger.error(f"Transfer failed: Source account {from_account_id} not found")
            raise AccountNotFoundError("Source account not found")
        if not to_account:
            logger.error(f"Transfer failed: Destination account {to_account_id} not found")
            raise AccountNotFoundError("Destination account not found")
        if from_account.balance < amount:
            logger.error(f"Transfer failed: Insufficient funds in source account {from_account_id}. Available balance: {from_account.balance}, requested: {amount}")
            raise InsufficientFundsError("Insufficient funds in source account")
        # Perform transfer
        new_from_balance = from_account.balance - amount
        new_to_balance = to_account.balance + amount
        self.db.update_balance(from_account_id, new_from_balance)
        self.db.update_balance(to_account_id, new_to_balance)
        logger.info(f"Transfer successful: {amount} transferred from account {from_account_id} to account {to_account_id}. New balances - Source: {new_from_balance}, Destination: {new_to_balance}")
        return {"from_new_balance": new_from_balance, "to_new_balance": new_to_balance}
    def delete_account(self, delete_request: DeleteAccountRequest):
        # Implementation logic to delete an account
        account_id = delete_request.account_id
        account = self.db.get_account(account_id)
        if not account:
            logger.error(f"Account deletion failed: Account {account_id} not found")
            raise AccountNotFoundError("Account not found")
        if account.balance != 0:
            logger.error(f"Account deletion failed: Account {account_id} has non-zero balance {account.balance}")
            raise AccountDeletionError("Account balance must be zero to delete")
        self.db.delete_account(account_id)
        logger.info(f"Account deletion successful: Account {account_id} deleted")
        return True
    def get_transaction_history(self, account_id: int):
        # Implementation logic to get transaction history for an account
        account = self.db.get_account(account_id)
        if not account:
            logger.error(f"Transaction history retrieval failed: Account {account_id} not found")
            raise AccountNotFoundError("Account not found")
        transactions = self.db.get_transactions(account_id)
        logger.info(f"Transaction history retrieval successful: Account {account_id} has {len(transactions)} transactions")
        return transactions
    def calculate_interest(self, interest_data: InterestCalculation):
        # Implementation logic to calculate interest for an account
        account_id = interest_data.account_id
        annual_rate = interest_data.annual_rate
        years = interest_data.years
        if annual_rate <= 0:
            logger.error(f"Interest calculation failed: Invalid annual rate {annual_rate} for account {account_id}")
            raise ValueError("Annual rate must be greater than zero")
        if years <= 0:
            logger.error(f"Interest calculation failed: Invalid number of years {years} for account {account_id}")
            raise ValueError("Number of years must be greater than zero")
        account = self.db.get_account(account_id)
        if not account:
            logger.error(f"Interest calculation failed: Account {account_id} not found")
            raise AccountNotFoundError("Account not found")
        # Simple interest calculation
        interest = account.balance * (annual_rate / 100) * years
        logger.info(f"Interest calculation successful: Account {account_id} will earn {interest} in interest over {years} years at an annual rate of {annual_rate}%")
        return interest
    