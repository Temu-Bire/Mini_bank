from calendar import c

class InsufficientFundsError(Exception):
    """Raised when an account has insufficient funds for a transaction."""
    pass
class AccountNotFoundError(Exception):
    """Raised when an account is not found in the system."""
    pass
class AccountDeletionError(Exception):
    """Raised when an account cannot be deleted due to existing balance or transactions."""
    pass
class InterestCalculationError(Exception):
    """Raised when there is an error in calculating interest."""
    pass
class TransactionHistoryError(Exception):
    """Raised when there is an error retrieving transaction history."""
    pass
class AccountCreationError(Exception):
    """Raised when there is an error creating a new account."""
    pass

