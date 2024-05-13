from pydantic import BaseModel


class AddUser(BaseModel):
    id: int
    address: str
    ref_id: int | None


class AddUserResponse(BaseModel):
    status: int
    detail: str


class UserResponse(BaseModel):
    id: int
    address: str
    balance: float
    contract: str
    claim_status: str
    time_to_claim: int
    refs: int
    daily_claim: int
    boost: int


class HTTPError(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            'example': {'detail': 'HTTPException raised when user not found'}
        }
