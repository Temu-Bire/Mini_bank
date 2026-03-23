from calendar import c


class InsufficientFundsError(Exception):
    """Raised when an account has insufficient funds for a transaction."""
    pass
class AccountNotFoundError(Exception):
    """Raised when an account is not found in the system."""
    pass
class InvalidTransferError(Exception):
    """Raised when a transfer request is invalid."""
    pass
class AuthenticationError(Exception):
    """Raised when user authentication fails."""
    pass
class AuthorizationError(Exception):
    """Raised when a user is not authorized to perform an action."""
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

