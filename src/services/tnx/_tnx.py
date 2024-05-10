from src.common import TonAPI
from src.utils.algs import get_tnx_balance
from ._gecko import gt


class TnxService(TonAPI):
    def __init__(self):
        super().__init__()
        self.tnx_addr = 'EQB-ajMyi5-WKIgOHnbOGApfckUGbl6tDk3Qt8PKmb-xLAvp'
        self.accounts = self.tonapi.accounts
        self.gt = gt

    async def get_tnx_price(self) -> float:
        tnx_price = float(await self.gt.get_token_price(token_addr=self.tnx_addr))

        return tnx_price

    async def get_tnx_balance(self, wallet_addr: str) -> str:
        jettons_balances = (await self.accounts.get_jettons_balances(account_id=wallet_addr)).balances

        tnx_balance = get_tnx_balance(jettons_balances=jettons_balances)

        if not tnx_balance:
            return '0'

        return f'{tnx_balance:.1f}'


tnx_service = TnxService()
