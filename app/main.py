import streamlit as st

from database.session import init_database
from services.listing_service import get_listings, save_listings
from scrapers.fake_scraper import FakeScraper


init_database()


st.set_page_config(
    page_title="Housing Assistant",
    page_icon="🏠",
)


st.title("🏠 Housing Assistant")


if st.button("Actualizar anuncios"):

    scraper = FakeScraper()

    listings = scraper.scrape()

    save_listings(listings)

    st.success(
        f"{len(listings)} anuncios actualizados"
    )


st.subheader("Anuncios")


listings = get_listings()


for listing in listings:

    st.write(
        f"""
        ### {listing.title}

        💶 {listing.price} €

        📍 {listing.neighborhood}

        🛏 {listing.bedrooms} habitaciones

        Fuente: {listing.source}

        {listing.url}
        """
    )