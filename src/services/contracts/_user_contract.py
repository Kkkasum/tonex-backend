import json

from pydantic import BaseModel, ConfigDict

from pytoniq import Contract, LiteClientLike
from pytoniq_core import Address, Cell, begin_cell

from src.common import USER_COMPILED_JSON_PATH, FIRST_CLAIM_AMOUNT
from ._models import UserContractOp


class UserConfig(BaseModel):
    admin_address: Address  # claim contract
    user_address: Address
    last_transaction_time: int = 0

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserContract(Contract):
    @staticmethod
    def code_hex() -> str:
        with open(USER_COMPILED_JSON_PATH) as data:
            compiled_json = json.load(data)

        return compiled_json['hex']

    @staticmethod
    def code_base64() -> str:
        with open(USER_COMPILED_JSON_PATH) as data:
            compiled_json = json.load(data)

        return compiled_json['hashBase64']

    @staticmethod
    def _user_config_to_cell(config: UserConfig) -> Cell:
        return (
            begin_cell()
            .store_address(config.admin_address)
            .store_ref(
                begin_cell()
                .store_address(config.user_address)
                .store_coins(FIRST_CLAIM_AMOUNT)
                .store_int(config.last_transaction_time, 64)
                .end_cell()
            )
            .end_cell()
        )

    @classmethod
    async def from_config(cls, provider: LiteClientLike, config: UserConfig, workchain: int = 0):
        code = Cell.one_from_boc(data=cls.code_hex())
        data = cls._user_config_to_cell(config=config)

        return await cls.from_code_and_data(provider=provider, workchain=workchain, code=code, data=data)

    @property
    def op(self) -> UserContractOp:
        return UserContractOp()
