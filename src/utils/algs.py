from pytonapi.schema.jettons import JettonBalance


def get_tnx_balance(jettons_balances: list[JettonBalance]) -> float | None:
    for jetton_balance in jettons_balances:
        if jetton_balance.jetton.symbol == 'TNX':
            return float(jetton_balance.balance) / 10 ** 9

    return None
