from pydantic import BaseModel


class Price(BaseModel):
    price: str


class Balance(BaseModel):
    balance: str = '0'
