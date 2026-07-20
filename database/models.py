from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Listing(Base):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True)

    source: Mapped[str] = mapped_column(String(50))

    title: Mapped[str] = mapped_column(String(300))

    neighborhood: Mapped[str] = mapped_column(String(100))

    price: Mapped[int]

    bedrooms: Mapped[int]

    url: Mapped[str] = mapped_column(String(1000))