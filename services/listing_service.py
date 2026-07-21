from database.models import Listing
from database.session import get_session
from services.normalizer import normalize_listing


def create_listing(
    source,
    title,
    price,
    neighborhood,
    district,
    bedrooms,
    bathrooms=None,
    surface_m2=None,
    furnished=None,
    available_from=None,
    url=None,
):

    session = get_session()

    existing = session.query(Listing).filter_by(
        url=url
    ).first()

    if existing:
        session.close()
        return

    listing = Listing(
        source=source,
        title=title,
        price=price,
        neighborhood=neighborhood,
        district=district,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        surface_m2=surface_m2,
        furnished=furnished,
        available_from=available_from,
        url=url,
    )

    session.add(listing)
    session.commit()
    session.close()


def save_listings(listings):

    for item in listings:

        item = normalize_listing(item)

        create_listing(
            source=item["source"],
            title=item["title"],
            price=item["price"],
            neighborhood=item["neighborhood"],
            district=item.get("district"),
            bedrooms=item["bedrooms"],
            bathrooms=item.get("bathrooms"),
            surface_m2=item.get("surface_m2"),
            furnished=item.get("furnished"),
            available_from=item.get("available_from"),
            url=item["url"],
        )


def get_listings():

    session = get_session()

    listings = session.query(Listing).all()

    session.close()

    return listings