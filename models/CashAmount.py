from pydantic import BaseModel

class CashAmount(BaseModel):
    amount: float