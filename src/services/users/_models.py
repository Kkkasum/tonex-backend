from pydantic import BaseModel


class AddUser(BaseModel):
    id: int
    address: str
    ref_id: int | None


class GetUser(BaseModel):
    id: int
    address: str
    balance: float
    contract: str
    claim_status: str
    time_to_claim: int
    refs: int
    boost: int
    daily_claim: int
