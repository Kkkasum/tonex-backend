from pytonapi import AsyncTonapi

from ._config import config


class TonAPI:
    def __init__(self):
        self.tonapi = AsyncTonapi(api_key=config.TON_API_KEY)
