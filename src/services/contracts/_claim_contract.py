import json

from pydantic import BaseModel, ConfigDict

from pytoniq import Contract, LiteClientLike
from pytoniq_core import Address, Cell, begin_cell

from src.common import CLAIM_COMPILED_JSON_PATH


class ClaimConfig(BaseModel):
    admin_address: Address = Address('UQA42cXENEQIFdyGn0LvkMATaTXVGKspTHalqReI9VKZPLhS')
    jetton_master_address: Address = Address('kQAyiCzg1aXZvo11trVJnpmJqD94egx6V1njV5fSlRCAPttg')
    jetton_wallet_code: Cell = Cell.one_from_boc(data='b5ee9c7201021101000323000114ff00f4a413f4bcf2c80b0102016202030202cc0405001ba0f605da89a1f401f481f481a8610201d40607020120080900c30831c02497c138007434c0c05c6c2544d7c0fc03383e903e900c7e800c5c75c87e800c7e800c1cea6d0000b4c7e08403e29fa954882ea54c4d167c0278208405e3514654882ea58c511100fc02b80d60841657c1ef2ea4d67c02f817c12103fcbc2000113e910c1c2ebcb853600201200a0b0083d40106b90f6a2687d007d207d206a1802698fc1080bc6a28ca9105d41083deecbef09dd0958f97162e99f98fd001809d02811e428027d012c678b00e78b6664f6aa401f1503d33ffa00fa4021f001ed44d0fa00fa40fa40d4305136a1522ac705f2e2c128c2fff2e2c254344270542013541403c85004fa0258cf1601cf16ccc922c8cb0112f400f400cb00c920f9007074c8cb02ca07cbffc9d004fa40f40431fa0020d749c200f2e2c4778018c8cb055008cf1670fa0217cb6b13cc80c0201200d0e009e8210178d4519c8cb1f19cb3f5007fa0222cf165006cf1625fa025003cf16c95005cc2391729171e25008a813a08209c9c380a014bcf2e2c504c98040fb001023c85004fa0258cf1601cf16ccc9ed5402f73b51343e803e903e90350c0234cffe80145468017e903e9014d6f1c1551cdb5c150804d50500f214013e809633c58073c5b33248b232c044bd003d0032c0327e401c1d3232c0b281f2fff274140371c1472c7cb8b0c2be80146a2860822625a019ad822860822625a028062849e5c412440e0dd7c138c34975c2c0600f1000d73b51343e803e903e90350c01f4cffe803e900c145468549271c17cb8b049f0bffcb8b08160824c4b402805af3cb8b0e0841ef765f7b232c7c572cfd400fe8088b3c58073c5b25c60063232c14933c59c3e80b2dab33260103ec01004f214013e809633c58073c5b3327b552000705279a018a182107362d09cc8cb1f5230cb3f58fa025007cf165007cf16c9718010c8cb0524cf165006fa0215cb6a14ccc971fb0010241023007cc30023c200b08e218210d53276db708010c8cb055008cf165004fa0216cb6a12cb1f12cb3fc972fb0093356c21e203c85004fa0258cf1601cf16ccc9ed54')

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
    def __claim_config_to_cell(config: ClaimConfig) -> Cell:
        return (
            begin_cell()
            .store_address(config.admin_address)
            .store_ref(
                begin_cell()
                .store_address(config.jetton_master_address)
                .store_ref(config.jetton_wallet_code)
                .end_cell()
            )
            .end_cell()
        )

    @classmethod
    async def from_config(cls, provider: LiteClientLike, workchain: int = 0):
        data: Cell = cls.__claim_config_to_cell(config=ClaimConfig())
        code: Cell = Cell.one_from_boc(data=cls.code_hex())

        return await cls.from_code_and_data(provider=provider, workchain=workchain, code=code, data=data)
