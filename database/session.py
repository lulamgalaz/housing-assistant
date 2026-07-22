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
    from database.models import Listing

    Base.metadata.create_all(bind=engine)

    def migrate_database():
    from sqlalchemy import text

    with engine.connect() as conn:

        columns = conn.execute(
            text("PRAGMA table_info(preferences)")
        ).fetchall()

        existing = [
            column[1]
            for column in columns
        ]

        migrations = {
            "profile_name": "ALTER TABLE preferences ADD COLUMN profile_name VARCHAR(100)",
            "min_surface": "ALTER TABLE preferences ADD COLUMN min_surface INTEGER",
            "duration_months": "ALTER TABLE preferences ADD COLUMN duration_months INTEGER",
        }

        for name, sql in migrations.items():

            if name not in existing:
                conn.execute(text(sql))

        conn.commit()