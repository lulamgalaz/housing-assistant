from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///housing.db"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

from database.models import Listing

Base.metadata.create_all(bind=engine)