from models.Signup import Signup
from pydantic import BaseModel

class CashAmount(Signup):
    amount: float
