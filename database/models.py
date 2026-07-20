from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Listing(Base):

    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    source: Mapped[str] = mapped_column(
        String(50)
    )

    title: Mapped[str] = mapped_column(
        String(300)
    )

    neighborhood: Mapped[str] = mapped_column(
        String(100)
    )

    price: Mapped[int]

    bedrooms: Mapped[int]

    bathrooms: Mapped[int | None]

    surface_m2: Mapped[int | None]

    furnished: Mapped[bool | None]

    available_from: Mapped[str | None]

    url: Mapped[str] = mapped_column(
        String(1000),
        unique=True
    )


class Preference(Base):

    __tablename__ = "preferences"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    city: Mapped[str] = mapped_column(
        String(100)
    )

    max_price: Mapped[int]

    min_bedrooms: Mapped[int]

    neighborhoods: Mapped[str] = mapped_column(
        String(300)
    )