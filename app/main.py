import sys
from pathlib import Path

# streamlit run ejecuta este archivo directo, y solo agrega la carpeta app/
# al sys.path (no la raiz del proyecto). Sin esto, "from database..." y
# "from services..." fallan con ModuleNotFoundError.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from database.session import init_database
from services.listing_service import get_listings, save_listings
from scrapers.pisos_scraper import PisosScraper
from services.preference_service import create_preference
from services.preference_service import get_preferences
from services.matcher import matches_preferences

# Barrios candidatos: buena conexion a Placa Catalunya (FGC hacia la UAB en
# Bellaterra) sin quedar demasiado lejos de la L4 (UPF Ciutadella/Poblenou).
# Es un punto de partida, no una lista cerrada -- ajustable a gusto.
BARRIOS_CANDIDATOS = [
    "Eixample",
    "Dreta de l'Eixample",
    "Esquerra de l'Eixample",
    "Gràcia",
    "Sant Antoni",
    "El Born",
    "Sant Pere",
    "Santa Caterina",
    "La Ribera",
    "Poblenou",
    "Poble Sec",
    "Montjuïc",
]

# Dos combinaciones validas: 2 hab. hasta 1200e, o 3 hab. hasta 1800e
PLANES_PRESUPUESTO = [
    {"bedrooms": 2, "max_price": 1200},
    {"bedrooms": 3, "max_price": 1800},
]

init_database()

st.set_page_config(
    page_title="Housing Assistant",
    page_icon="🏠",
    layout="wide",
)

st.markdown(
    """
    <style>
    .listing-card {
        background-color: #1C1F26;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }
    .listing-title {
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
        color: #FAFAFA;
    }
    .listing-price {
        font-size: 1.4rem;
        font-weight: 700;
        color: #A78BFA;
    }
    .listing-meta {
        color: #B5B9C4;
        font-size: 0.95rem;
        margin-top: 0.35rem;
    }
    .listing-badge {
        display: inline-block;
        background-color: rgba(124, 92, 255, 0.15);
        color: #A78BFA;
        border-radius: 999px;
        padding: 0.15rem 0.7rem;
        font-size: 0.8rem;
        margin-right: 0.4rem;
    }
    .listing-link a {
        color: #7C5CFF;
        text-decoration: none;
        font-weight: 500;
    }
    .listing-link a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏠 Housing Assistant")
st.caption("Búsqueda de departamentos en Barcelona, filtrada por barrio y presupuesto")

col1, col2 = st.columns(2)

with col1:
    if st.button("💾 Guardar búsqueda", use_container_width=True):
        create_preference(
            city="Barcelona",
            neighborhoods=BARRIOS_CANDIDATOS,
            plans=PLANES_PRESUPUESTO,
        )
        st.success("Búsqueda guardada")

with col2:
    if st.button("🔄 Actualizar anuncios", use_container_width=True):
        scraper = PisosScraper(city="barcelona_capital", max_pages=2)
        listings = scraper.scrape()
        save_listings(listings)
        st.success(f"{len(listings)} anuncios actualizados")

st.divider()
st.subheader("Anuncios")

listings = get_listings()
preferences = get_preferences()

if preferences:
    preference = preferences[-1]
    listings = [
        listing
        for listing in listings
        if matches_preferences(listing, preference)
    ]

if not listings:
    st.info("No hay anuncios todavía. Tocá \"Guardar búsqueda\" y después \"Actualizar anuncios\".")

for listing in listings:
    st.markdown(
        f"""
        <div class="listing-card">
            <div class="listing-title">{listing.title}</div>
            <div class="listing-price">{listing.price} € / mes</div>
            <div class="listing-meta">
                <span class="listing-badge">📍 {listing.neighborhood}</span>
                <span class="listing-badge">🛏 {listing.bedrooms} hab.</span>
                <span class="listing-badge">Fuente: {listing.source}</span>
            </div>
            <div class="listing-meta listing-link">
                <a href="{listing.url}" target="_blank">Ver anuncio →</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )