import asyncio
from time import time

from pytoniq import LiteClientLike, HighloadWallet, LiteServerError
from pytoniq_core import Address, begin_cell, Cell
from pytonapi.utils import amount_to_nano

from loguru import logger

from src.common import FIRST_CLAIM_AMOUNT
from ._provider import Providers
from ._claim_contract import ClaimContract
from ._user_contract import UserContract, UserConfig
from ._models import Chain, ClaimStatus, UserContractData, ClaimData
from ._wallet import Wallet


class ContractsService:
    def __init__(self):
        self.chain: Chain = Chain.TESTNET
        self.provider: LiteClientLike = Providers(self.chain).cur_provider

    @staticmethod
    async def _create_user_contract(provider: LiteClientLike, admin_address: Address, user_wallet: str) -> UserContract:
        config = UserConfig(
            admin_address=admin_address,
            user_address=Address(user_wallet)
        )

        return await UserContract.from_config(provider=provider, config=config)

    @staticmethod
    async def _get_highload(provider: LiteClientLike) -> HighloadWallet:
        highload_wallet = await Wallet.create_admin_highload(provider=provider)
        wallet = await Wallet.create_admin(provider=provider)

        highload_wallet_balance = await highload_wallet.get_balance()

        # deposit ton if low balance
        if highload_wallet_balance < amount_to_nano(0.2):
            await wallet.transfer(destination=highload_wallet.address, amount=amount_to_nano(0.2))

        while highload_wallet_balance < amount_to_nano(0.2):
            highload_wallet_balance = await highload_wallet.get_balance()

        if highload_wallet.account.state.type_ == 'uninitialized':
            try:
                await highload_wallet.deploy_via_external()
            except LiteServerError as e:
                if e.code != 0:
                    logger.error(e)

        await asyncio.sleep(5)

        return highload_wallet

    async def first_claim(self, user_wallet: str):
        highload_wallet = await self._get_highload(provider=self.provider)
        claim_contract = await ClaimContract.from_config(provider=self.provider, admin_address=highload_wallet.address)
        user_contract = await self._create_user_contract(
            provider=self.provider,
            admin_address=claim_contract.contract_address,
            user_wallet=user_wallet
        )

        print(highload_wallet.address)
        print(claim_contract.address)
        print(user_contract.address)

        claim_body = (
            begin_cell()
                .store_uint(claim_contract.op.first_claim, 32)
                .store_uint(0, 64)
                .store_coins(FIRST_CLAIM_AMOUNT)
                .store_address(user_wallet)
            .end_cell()
        )

        claim_contract_address = Address('kQDYZaKkR_R9xg9vEETC6bJ7wkttJOC1MxU_SZ-UF0HqinES')
        user_contract_address = Address('kQBxE30u-Is4onmAKUFmqGjtmJBmuQtVd73Es6kv3lrB6Wll')

        await highload_wallet.transfer(
            destinations=[claim_contract_address, user_contract_address],
            amounts=[amount_to_nano(0.1), amount_to_nano(0.05)],
            bodies=[claim_body, Cell.empty()],
            state_inits=[None, user_contract.state_init]
        )

    async def _get_user_contract(self, provider: LiteClientLike, user_wallet: str) -> UserContract:
        highload_wallet = await self._get_highload(provider=self.provider)
        claim_contract = await ClaimContract.from_config(provider=provider, admin_address=highload_wallet.address)
        config = UserConfig(
            admin_address=claim_contract.address,
            user_address=Address(user_wallet)
        )

        user_contract = await UserContract.from_config(provider=provider, config=config)

        return user_contract

    @staticmethod
    async def _get_claim_data(user_contract: UserContract) -> ClaimData:
        if user_contract.account.state.type_ == 'uninitialized':
            return ClaimData(
                claim_status=ClaimStatus.FIRST_CLAIM,
                time_to_claim=0
            )

        last_transaction_time = (
            await user_contract.run_get_method(method='get_last_transaction_time', stack=[])
        ).pop()

        if last_transaction_time == 0:
            return ClaimData(
                claim_status=ClaimStatus.FIRST_CLAIM,
                time_to_claim=0
            )

        time_diff = time() - last_transaction_time

        if time_diff >= 86400:
            return ClaimData(
                claim_status=ClaimStatus.READY,
                time_to_claim=0
            )

        return ClaimData(
            claim_status=ClaimStatus.NOT_YET,
            time_to_claim=time_diff
        )

    async def get_contract_data(self, user_wallet: str) -> UserContractData:
        try:
            user_contract = await self._get_user_contract(provider=self.provider, user_wallet=user_wallet)
            claim_data = await self._get_claim_data(user_contract=user_contract)
        except ConnectionError:
            await self.provider.start_up()
            user_contract = await self._get_user_contract(provider=self.provider, user_wallet=user_wallet)
            claim_data = await self._get_claim_data(user_contract=user_contract)

        return UserContractData(
            address=user_contract.address,
            claim_status=claim_data.claim_status,
            time_to_claim=claim_data.time_to_claim
        )


contracts_service = ContractsService()
