from time import time

from pytoniq import LiteClientLike, HighloadWallet
from pytoniq_core import Address, begin_cell
from pytonapi.utils import amount_to_nano

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

        user_contract = await UserContract.from_config(provider=provider, config=config)
        if user_contract.account.state.type_ == 'uninitialized':
            return user_contract

    @staticmethod
    async def _get_highload(provider: LiteClientLike) -> HighloadWallet:
        highload_wallet = await Wallet.create_highload(provider=provider)
        if highload_wallet.account.state.type_ == 'uninitialized':
            wallet = await Wallet.create_main(provider=provider)
            highload_wallet_balance = await highload_wallet.get_balance()

            # deposit ton if low balance
            if highload_wallet_balance < amount_to_nano(0.05):
                status = await wallet.transfer(destination=highload_wallet.address, amount=amount_to_nano(0.05))
                print(status)
            await highload_wallet.deploy_via_external()

        return highload_wallet

    async def deploy_user_contracts(self, wallets: list[str]) -> None:
        claim_contract = await ClaimContract.from_config(provider=self.provider)

        user_contracts = [
            (
                await self._create_user_contract(
                    provider=self.provider,
                    admin_address=claim_contract.address,
                    user_wallet=wallet
                )
            )
            for wallet in wallets
        ]
        user_contracts_addresses = [user_contract.address for user_contract in user_contracts]

        highload_wallet = await self._get_highload(provider=self.provider)

        amounts = [amount_to_nano(0.15) * len(user_contracts)]
        bodies = [begin_cell().end_cell() * len(user_contracts)]

        await highload_wallet.transfer(destinations=user_contracts_addresses, amounts=amounts, bodies=bodies)
        [
            await user_contract.deploy_via_external()
            for user_contract in user_contracts
        ]

    @staticmethod
    async def _get_user_contract(provider: LiteClientLike, user_wallet: str) -> UserContract:
        claim_contract = await ClaimContract.from_config(provider=provider)
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
