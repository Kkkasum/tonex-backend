import aiohttp


class GeckoTerminal:
    def __init__(self, api_url: str):
        self.api_url = api_url

    async def get_token_price(self, token_addr: str) -> str | None:
        url = self.api_url + f'/networks/ton/tokens/{token_addr}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url=url) as resp:
                if resp.status != 200:
                    return None

                res = await resp.json()

            return res['data']['attributes']['price_usd']


gt = GeckoTerminal(api_url='https://api.geckoterminal.com/api/v2')
