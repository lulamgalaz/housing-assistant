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
    page_title="Scout",
    page_icon="🏠",
    layout="wide",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&family=Space+Grotesk:wght@300..700&family=Courier+Prime:ital,wght@0,400;0,700;1,400;1,700&display=swap');

    h1 {
    font-family: "Outfit", sans-serif;
    font-optical-sizing: auto;
    font-weight: 700;
    font-size: 3.5rem;
    font-style: normal;
    text-align: center;
}
    h2 {
        font-family: "Space Grotesk", sans-serif;
        font-optical-sizing: auto;
        font-weight: 700;
        font-style: normal;
    }
    p {
        font-family: "Courier Prime", monospace;
        font-weight: 400;
        font-style: normal;
    }

[data-testid="stCaptionContainer"] {
    text-align: center;
}
    .listings-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
        gap: 0.75rem;
    }
    .listing-card {
        background-color: #1C1F26;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 0.85rem 1rem;
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
        overflow-wrap: break-word;
        word-break: break-word;
        min-width: 0;
    }
    .listing-title {
        font-family: "Courier Prime", monospace;
        font-size: 0.95rem;
        font-weight: 700;
        color: #FAFAFA;
        line-height: 1.25;
        overflow-wrap: break-word;
        word-break: break-word;
    }
    .listing-price {
        font-size: 1.1rem;
        font-weight: 700;
        color: #A78BFA;
    }
    .listing-meta {
        color: #B5B9C4;
        font-size: 0.8rem;
        overflow-wrap: break-word;
        word-break: break-word;
    }
    .listing-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 0.3rem;
    }
    .listing-badge {
        background-color: rgba(124, 92, 255, 0.15);
        color: #A78BFA;
        border-radius: 999px;
        padding: 0.1rem 0.55rem;
        font-size: 0.72rem;
        max-width: 100%;
        overflow-wrap: break-word;
        word-break: break-word;
        white-space: normal;
    }
    .listing-link a {
        color: #7C5CFF;
        text-decoration: none;
        font-weight: 500;
        font-size: 0.85rem;
    }
    .listing-link a:hover {
        text-decoration: underline;
    }

    @media (max-width: 480px) {
        .listings-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Scout", anchor=False)
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
st.header("Anuncios")

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

cards_html = "".join(
    "<div class=\"listing-card\">"
    f"<div class=\"listing-title\">{listing.title}</div>"
    f"<div class=\"listing-price\">{listing.price} €/mes</div>"
    "<div class=\"listing-badges\">"
    f"<span class=\"listing-badge\">📍 {listing.neighborhood}</span>"
    f"<span class=\"listing-badge\">🛏 {listing.bedrooms} hab.</span>"
    "</div>"
    f"<div class=\"listing-meta\">{listing.source}</div>"
    f"<div class=\"listing-link\"><a href=\"{listing.url}\" target=\"_blank\">Ver anuncio →</a></div>"
    "</div>"
    for listing in listings
)

st.markdown(
    f'<div class="listings-grid">{cards_html}</div>',
    unsafe_allow_html=True,
)