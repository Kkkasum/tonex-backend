from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import BIGINT, String, text


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True)
    address: Mapped[str] = mapped_column(String(48), unique=True)
    ref_id: Mapped[int | None] = mapped_column(BIGINT)
    daily_claim: Mapped[int] = mapped_column(server_default=text('0'))
    boost: Mapped[int] = mapped_column(server_default=text('0'))
