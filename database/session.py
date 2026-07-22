from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base


DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATA_DIR / "housing.db"


engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    echo=False,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_session():
    return SessionLocal()


def init_database():

    from database.models import Listing, Preference

    Base.metadata.create_all(
        bind=engine
    )