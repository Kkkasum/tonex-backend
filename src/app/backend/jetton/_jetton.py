from fastapi import APIRouter

from src.services.tnx import tnx_service
from ._schemas import Price, Balance


router = APIRouter()


@router.get('/tnx_price', response_model=Price)
async def get_tnx_price():
    tnx_price = await tnx_service.get_tnx_price()

    return Price(
        price=f'{tnx_price:.2f}'
    )


@router.get('/tnx_balance/{user_id}', response_model=Balance)
async def get_tnx_balance(wallet_addr: str):
    tnx_balance = await tnx_service.get_tnx_balance(wallet_addr=wallet_addr)
    if not tnx_balance:
        return Balance()

    return Balance(
        balance=f'{tnx_balance / 10 ** 9:.1f}'
    )
