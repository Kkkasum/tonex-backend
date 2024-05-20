from pytoniq import LiteBalancer

from ._models import Chain


class Providers:
    def __init__(self, chain: Chain):
        self.providers = {
            Chain.MAINNET: MainnetProvider(),
            Chain.TESTNET: TestnetProvider()
        }
        # self.cur_provider = self.providers[self.chain]
        self.cur_provider = self.providers[chain].provider


class MainnetProvider:
    def __init__(self):
        self.provider = LiteBalancer.from_mainnet_config(1)

    # async def __aenter__(self) -> LiteBalancer:
    #     await self.provider.start_up()
    #     return self.provider
    #
    # async def __aexit__(self, exc_type, exc_val, exc_tb):
    #     await self.provider.close_all()


class TestnetProvider:
    def __init__(self):
        self.provider = LiteBalancer.from_testnet_config(1)

    # async def __aenter__(self) -> LiteBalancer:
    #     await self.provider.start_up()
    #     return self.provider
    #
    # async def __aexit__(self, exc_type, exc_val, exc_tb):
    #     await self.provider.close_all()
