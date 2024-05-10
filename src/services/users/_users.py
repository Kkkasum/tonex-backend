from src.repos.users import UsersRepo
from src.services.tnx import tnx_service
from src.services.contracts import contracts_service
from ._models import AddUser, GetUser


class UsersService:
    def __init__(self):
        self.repo = UsersRepo()

    async def add_user(self, user: AddUser) -> None:
        await self.repo.add_user(user_id=user.id, address=user.address, ref_id=user.ref_id)

    async def get_user(self, user_id: int) -> GetUser:
        user = await self.repo.get_user(user_id=user_id)
        balance = await tnx_service.get_tnx_balance(wallet_addr=user[0])
        contract_data = await contracts_service.get_contract_data(user_wallet=user[0])

        return GetUser(
            id=user_id,
            address=user[0],
            balance=balance,
            contract=contract_data.address.to_str(is_user_friendly=True),
            claim_status=contract_data.claim_status,
            time_to_claim=contract_data.time_to_claim,
            refs=user[1],
            daily_claim=user[2],
            boost=user[3],
        )


users_service = UsersService()
