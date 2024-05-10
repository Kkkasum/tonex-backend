from enum import StrEnum

from pydantic import BaseModel, ConfigDict

from pytoniq_core import Address


class Chain(StrEnum):
    MAINNET = 'MAINNET'
    TESTNET = 'TESTNET'


class ClaimStatus(StrEnum):
    READY = 'READY'
    NOT_YET = 'NOT_YET'
    FIRST_CLAIM = 'FIRST_CLAIM'


class ClaimData(BaseModel):
    claim_status: ClaimStatus
    time_to_claim: float


class UserContractData(BaseModel):
    address: Address
    claim_status: ClaimStatus
    time_to_claim: float

    model_config = ConfigDict(arbitrary_types_allowed=True)
