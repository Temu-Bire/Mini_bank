
from pydantic import BaseModel, Field, field_validator, PositiveInt
class CreateAccount(BaseModel):
    owner_name: str = Field(..., min_length=3, max_length=100, pattern=r'^[a-zA-Z\s]+$')
    account_number: int = Field(..., ge=100, le=999999999)
    initial_deposit: float = Field(..., ge=0)
class Deposit(BaseModel):
    account_number: int = Field(..., ge=1)
    amount: float = Field(..., gt=0)
class Withdraw(BaseModel):
    account_number: int = Field(..., ge=1)
    amount: float = Field(..., gt=0)
class BalanceResponse(BaseModel):
    account_number: int = Field(..., ge=1)
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
class CurrencyConversionRequest(BaseModel):
    from_currency: str = Field(..., min_length=3, max_length=3, pattern=r'^[A-Z]+$')
    to_currency: str = Field(..., min_length=3, max_length=3, pattern=r'^[A-Z]+$')
    amount: float = Field(..., gt=0)

class CurrencyConversionResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
    rate: float
    date: str
