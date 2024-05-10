import json

from pydantic import BaseModel, ConfigDict

from pytoniq import Contract, LiteClientLike
from pytoniq_core import Address, Cell, begin_cell
from pytonapi.utils import amount_to_nano

from src.common import USER_COMPILED_JSON_PATH


class Opcodes(BaseModel):
    deposit: int = 0x95db9d39
    claim: int = 0xa769de27
    boost: int = 0x56642768
    change_admin: int = 0xd4deb03b


class UserConfig(BaseModel):
    admin_address: Address
    user_address: Address

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
                .store_coins(amount_to_nano(1))
                .store_int(0, 64)
                .end_cell()
            )
            .end_cell()
        )

    @classmethod
    async def from_config(cls, provider: LiteClientLike, config: UserConfig, workchain: int = 0):
        data: Cell = cls._user_config_to_cell(config=config)
        code: Cell = Cell.one_from_boc(data=cls.code_hex())

        return await cls.from_code_and_data(provider=provider, workchain=workchain, code=code, data=data)
