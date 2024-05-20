from sqlalchemy import select, insert, func

from src.database import Database, User


class UsersRepo(Database):
    def __init__(self):
        super().__init__()

    async def add_user(self, user_id: int, address: str, ref_id: int | None) -> None:
        async with self.session_maker() as session:
            stmt = insert(User)\
                .values(id=user_id, address=address, ref_id=ref_id)
            await session.execute(stmt)
            await session.commit()

    async def get_user(self, user_id: int) -> [str, int, int, int]:
        async with self.session_maker() as session:
            query = select(func.count(User.id))\
                .where(User.ref_id == user_id)
            res = await session.execute(query)
            refs = res.scalar()

            query = select(User.address, User.daily_claim, User.boost)\
                .where(User.id == user_id)
            res = (await session.execute(query)).first()

            return res[0], refs, res[1], res[2]

    async def get_user_wallet(self, user_id: int) -> str:
        async with self.session_maker() as session:
            query = select(User.address)\
                .where(User.id == user_id)
            res = (await session.execute(query)).first()

            return res[0]

    async def get_user_wallets(self) -> list[str]:
        async with self.session_maker() as session:
            query = select(User.contract)
            res = (await session.execute(query)).fetchall()

            return res
