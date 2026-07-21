import streamlit as st

from database.session import init_database

from services.listing_service import (
    get_listings,
    save_listings,
)

from services.preference_service import (
    create_preference,
    get_preferences,
)

from services.matcher import matches_preferences

from scrapers.pisos_scraper import PisosScraper


# Inicializar la base de datos
init_database()


# Configuración de Streamlit
st.set_page_config(
    page_title="Housing Assistant",
    page_icon="🏠",
)


st.title("🏠 Housing Assistant")


# -----------------------------
# Guardar preferencias
# -----------------------------
if st.button("Guardar búsqueda"):

    create_preference(
        city="Barcelona",
        max_price=1200,
        min_bedrooms=2,
        neighborhoods="Gràcia,Eixample",
    )

    st.success("Búsqueda guardada")


# -----------------------------
# Actualizar anuncios
# -----------------------------
if st.button("Actualizar anuncios"):

    scraper = PisosScraper(
        city="barcelona_capital",
        max_pages=1,
    )

    listings = scraper.scrape()

    save_listings(listings)

    st.success(
        f"{len(listings)} anuncios actualizados"
    )


# -----------------------------
# Mostrar anuncios
# -----------------------------
st.subheader("Anuncios")

listings = get_listings()
preferences = get_preferences()


if preferences:

    preference = preferences[-1]

    listings = [
        listing
        for listing in listings
        if matches_preferences(
            listing,
            preference,
        )
    ]


for listing in listings:

    st.write(
        f"""
### {listing.title}

💶 **{listing.price} €**

📍 {listing.neighborhood}

🛏 {listing.bedrooms} habitaciones

**Fuente:** {listing.source}

{listing.url}
"""
    )