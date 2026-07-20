from database.session import get_session
from database.models import Preference


def create_preference(
    city,
    max_price,
    min_bedrooms,
    neighborhoods,
):

    session = get_session()

    preference = Preference(
        city=city,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
        neighborhoods=neighborhoods,
    )

    session.add(preference)
    session.commit()
    session.close()


def get_preferences():

    session = get_session()

    preferences = session.query(Preference).all()

    session.close()

    return preferences