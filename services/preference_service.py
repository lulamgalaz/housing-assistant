from database.session import get_session
from database.models import Preference
from config.profile import SEARCH_PROFILES


def create_preference(
    profile_name,
    city,
    neighborhoods,
):

    if profile_name not in SEARCH_PROFILES:

        raise ValueError(
            f"Perfil inexistente: {profile_name}"
        )


    profile = SEARCH_PROFILES[profile_name]


    session = get_session()


    preference = Preference(

        profile_name=profile_name,

        city=city,

        max_price=profile["max_price"],

        min_bedrooms=profile["min_bedrooms"],

        min_surface=profile.get(
            "min_surface"
        ),

        duration_months=profile.get(
            "duration_months"
        ),

        neighborhoods=", ".join(
            neighborhoods
        ),
    )


    session.add(preference)

    session.commit()

    session.close()



def get_preferences():

    session = get_session()

    preferences = (
        session
        .query(Preference)
        .order_by(Preference.id.asc())
        .all()
    )

    session.close()

    return preferences