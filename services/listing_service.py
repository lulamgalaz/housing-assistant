from database.models import Listing
from database.session import get_session


def create_listing(
    source,
    title,
    price,
    neighborhood,
    bedrooms,
    url,
):
    session = get_session()

    listing = Listing(
        source=source,
        title=title,
        price=price,
        neighborhood=neighborhood,
        bedrooms=bedrooms,
        url=url,
    )

    session.add(listing)
    session.commit()
    session.close()


def save_listings(listings):

    for item in listings:

        create_listing(
            source=item["source"],
            title=item["title"],
            price=item["price"],
            neighborhood=item["neighborhood"],
            bedrooms=item["bedrooms"],
            url=item["url"],
        )


def get_listings():

    session = get_session()

    listings = session.query(Listing).all()

    session.close()

    return listings