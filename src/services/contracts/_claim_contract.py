import json

from pydantic import BaseModel, ConfigDict

from pytoniq import Contract, LiteClientLike
from pytoniq_core import Address, Cell, begin_cell

from src.common import CLAIM_COMPILED_JSON_PATH
from ._models import Jetton, ClaimContractOp
from ._user_contract import UserContract


class ClaimConfig(BaseModel):
    admin_address: Address  # highload
    jetton_master_address: Address = Jetton().jetton_master_address
    jetton_wallet_code: Cell = Jetton().jetton_wallet_code
    user_contract_code: Cell = Cell.one_from_boc(data=UserContract.code_hex())

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ClaimContract(Contract):
    @staticmethod
    def code_hex() -> str:
        with open(CLAIM_COMPILED_JSON_PATH) as data:
            compiled_json = json.load(data)

        return compiled_json['hex']

    @staticmethod
    def code_base64() -> str:
        with open(CLAIM_COMPILED_JSON_PATH) as data:
            compiled_json = json.load(data)

        return compiled_json['hashBase64']

    @staticmethod
    def _claim_config_to_cell(config: ClaimConfig) -> Cell:
        return (
            begin_cell()
            .store_address(config.admin_address)
            .store_ref(
                begin_cell()
                .store_address(config.jetton_master_address)
                .store_ref(config.jetton_wallet_code)
                .end_cell()
            )
            .store_ref(config.user_contract_code)
            .end_cell()
        )

    @classmethod
    async def from_config(cls, provider: LiteClientLike, admin_address: Address, workchain: int = 0):
        code = Cell.one_from_boc(data=cls.code_hex())
        data = cls._claim_config_to_cell(
            config=ClaimConfig(
                admin_address=admin_address
            )
        )

        return await cls.from_code_and_data(provider=provider, workchain=workchain, code=code, data=data)

    @property
    def op(self) -> ClaimContractOp:
        return ClaimContractOp()

    @property
    def contract_address(self) -> Address:
        return Address('kQDYZaKkR_R9xg9vEETC6bJ7wkttJOC1MxU_SZ-UF0HqinES')
