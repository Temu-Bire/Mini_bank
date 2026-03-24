
from pydantic import BaseModel, Field, field_validator, PositiveInt
class CreateAccount(BaseModel):
    owner_name: str = Field(..., min_length=3, max_length=100)
    account_number: int = Field(..., min_length=3, max_length=20)
    initial_deposit: float = Field(..., ge=0)
class Deposit(BaseModel):
    account_number: int = Field(..., ge=1)
    amount: float = Field(..., gt=0)
class Withdraw(BaseModel):
    account_number: int = Field(..., ge=1)
    amount: float = Field(..., gt=0)
class BalanceResponse(BaseModel):
    account_number: int = Field(..., ge=1)
    balance: float
class TransferRequest(BaseModel):
    from_account_number: int = Field(..., ge=1)
    to_account_number: int = Field(..., ge=1)
    amount: float = Field(..., gt=0)
class DeleteAccountRequest(BaseModel):
    account_number: int = Field(..., ge=1)
class TransactionHistory(BaseModel):
    account_number: int = Field(..., ge=1)
    transactions: list[str]
class InterestCalculation(BaseModel):
    account_number: int = Field(..., ge=1)
    annual_rate: float = Field(..., gt=0)
    years: int = Field(..., ge=1)
