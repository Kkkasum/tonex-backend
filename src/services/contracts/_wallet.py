import os
import json

from pytoniq import HighloadWallet, WalletV4, WalletV4R2, LiteClientLike, Contract

from src.common import HIGHLOAD_MNEMO_PATH, MAIN_MNEMO_PATH


class Wallet(Contract):
    @staticmethod
    def save_mnemo(file_path: str, mnemo: list[str]) -> None:
        with open(file_path, 'a') as f:
            mnemo_json = {
                i: word
                for i, word in enumerate(mnemo)
            }

            json.dump(mnemo_json, f)

    @staticmethod
    def get_mnemo(file_path: str) -> list[str]:
        with open(file_path, 'r') as f:
            mnemo_json = json.load(f)
            mnemo = [word for word in mnemo_json.values()]

            return mnemo

    @classmethod
    async def create_highload(cls, provider: LiteClientLike) -> HighloadWallet:
        if not os.path.isfile(HIGHLOAD_MNEMO_PATH):
            mnemo, highload_wallet = await HighloadWallet.create(provider=provider)
            cls.save_mnemo(HIGHLOAD_MNEMO_PATH, mnemo)
        else:
            mnemo = cls.get_mnemo(HIGHLOAD_MNEMO_PATH)
            highload_wallet = await HighloadWallet.from_mnemonic(provider=provider, mnemonics=mnemo)

        return highload_wallet

    @classmethod
    async def create_main(cls, provider: LiteClientLike) -> WalletV4:
        mnemo = cls.get_mnemo(MAIN_MNEMO_PATH)

        return await WalletV4R2.from_mnemonic(provider=provider, mnemonics=mnemo)
