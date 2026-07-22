from sqlalchemy import text

from database.session import engine


def migrate_preferences():

    with engine.connect() as connection:

        existing_columns = connection.execute(
            text("PRAGMA table_info(preferences)")
        ).fetchall()

        columns = [
            column[1]
            for column in existing_columns
        ]

        migrations = {
            "profile_name": "ALTER TABLE preferences ADD COLUMN profile_name VARCHAR(100)",
            "min_surface": "ALTER TABLE preferences ADD COLUMN min_surface INTEGER",
            "duration_months": "ALTER TABLE preferences ADD COLUMN duration_months INTEGER",
        }

        for column_name, sql in migrations.items():

            if column_name not in columns:

                connection.execute(
                    text(sql)
                )

                print(
                    f"Agregada columna: {column_name}"
                )

            else:

                print(
                    f"Ya existe: {column_name}"
                )

        connection.commit()


if __name__ == "__main__":

    migrate_preferences()

    print(
        "Migración completada"
    )