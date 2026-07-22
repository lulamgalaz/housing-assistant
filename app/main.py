import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

import streamlit as st

from config.profile import SEARCH_PROFILES

from services.listing_service import get_listings
from services.preference_service import (
    create_preference,
    get_preferences,
)
from services.matcher import matches_preferences
from services.search_service import update_all_sources
from database.session import init_database
init_database()

favicon = Path(__file__).parent / "favicon.png"


st.set_page_config(
    page_title="Scout",
    page_icon=str(favicon),
    layout="wide",
)


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


st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&family=Space+Grotesk:wght@300..700&family=Courier+Prime:wght@400;700&display=swap');


    h1 {
        font-family: "Outfit", sans-serif;
        font-weight: 700;
        font-size: 5rem !important;
        text-align: center;
    }


    h2 {
        font-family: "Space Grotesk", sans-serif;
        font-weight: 700;
        font-size: 2.5rem !important;
        text-align: center;
    }


    p {
        font-family: "Courier Prime", monospace;
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
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 0.85rem 1rem;
        display:flex;
        flex-direction:column;
        gap:0.3rem;
    }


    .listing-title {
        font-family:"Courier Prime", monospace;
        font-size:0.95rem;
        font-weight:700;
        color:#FAFAFA;
    }


    .listing-price {
        font-size:1.1rem;
        font-weight:700;
        color:#A78BFA;
    }


    .listing-meta {
        color:#B5B9C4;
        font-size:0.8rem;
    }


    .listing-badges {
        display:flex;
        flex-wrap:wrap;
        gap:0.3rem;
    }


    .listing-badge {
        background-color:rgba(124,92,255,0.15);
        color:#A78BFA;
        border-radius:999px;
        padding:0.1rem 0.55rem;
        font-size:0.72rem;
    }


    .listing-link a {
        color:#7C5CFF;
        text-decoration:none;
        font-size:0.85rem;
    }


    </style>
    """,
    unsafe_allow_html=True,
)


st.title(
    "Scout",
    anchor=False
)


st.caption(
    "Búsqueda de departamentos en Barcelona, filtrada por perfil"
)


# -------------------------
# Selector de perfil
# -------------------------

profile_name = st.selectbox(
    "Perfil de búsqueda",
    options=list(SEARCH_PROFILES.keys()),
)


selected_profile = SEARCH_PROFILES[profile_name]


st.info(
    f"""
**{profile_name}**

💶 Máximo: {selected_profile["max_price"]} €/mes

🛏 Habitaciones: {selected_profile["min_bedrooms"]}

📐 Superficie mínima: {selected_profile["min_surface"]} m²

📅 Duración: {selected_profile["duration_months"]} meses
"""
)


col1, col2 = st.columns(2)


with col1:

    if st.button(
        "💾 Guardar búsqueda",
        use_container_width=True,
    ):

        create_preference(
            profile_name=profile_name,
            city="Barcelona",
            neighborhoods=BARRIOS_CANDIDATOS,
        )

        st.session_state["active_profile"] = profile_name

        st.success(
            f"Búsqueda guardada: {profile_name}"
        )


with col2:

    if st.button(
        "🔄 Actualizar anuncios",
        use_container_width=True,
    ):

        result = update_all_sources()

        st.success(
            f"{result['total']} anuncios actualizados"
        )


st.divider()


st.header(
    "Anuncios"
)


listings = get_listings()
listings = get_listings()
preferences = get_preferences()

st.write(f"Anuncios: {len(listings)}")
st.write(f"Preferencias: {len(preferences)}")

ranked_listings = []

if preferences:

    preference = preferences[-1]

    st.write("### Preferencia activa")
    st.write(f"Perfil: {preference.profile_name}")
    st.write(f"Ciudad: {preference.city}")
    st.write(f"Precio máximo: {preference.max_price}")
    st.write(f"Habitaciones mínimas: {preference.min_bedrooms}")
    st.write(f"Superficie mínima: {preference.min_surface}")
    st.write(f"Duración: {preference.duration_months}")
    st.write(f"Barrios: {preference.neighborhoods}")

    for listing in listings:

        result = matches_preferences(
            listing,
            preference,
        )

        print(
            listing.title,
            listing.price,
            listing.bedrooms,
            result["match"],
            result["score"],
            result["reasons"],
        )

        st.write(
            listing.title,
            result["match"],
            result["reasons"],
        )

        if result["match"]:

            ranked_listings.append(
                {
                    "listing": listing,
                    "score": result["score"],
                    "reasons": result["reasons"],
                }
            )

ranked_listings.sort(
    key=lambda x: x["score"],
    reverse=True,
            )

listings = ranked_listings

st.write(f"Anuncios filtrados: {len(listings)}")
 
if not listings:

    st.info(
        'No hay anuncios. Guardá una búsqueda y actualizá.'
    )

st.write("Anuncios:", len(get_listings()))
st.write("Preferencias:", len(get_preferences()))

cards_html = "".join(

                        "<div class=\"listing-card\">">

    f"<div class=\"listing-title\">#{index} — {item['listing'].title}</div>"

    f"<div class=\"listing-price\">⭐ {item['score']} puntos</div>"

    f"<div class=\"listing-meta\">{item['listing'].price} €/mes</div>"

    "<div class=\"listing-badges\">"

    f"<span class=\"listing-badge\">📍 {item['listing'].neighborhood}</span>"

    f"<span class=\"listing-badge\">🛏 {item['listing'].bedrooms} hab.</span>"

    "</div>"

    f"<div class=\"listing-meta\">{item['listing'].source}</div>"

    f"<div class=\"listing-link\"><a href=\"{item['listing'].url}\" target=\"_blank\">Ver anuncio →</a></div>"

    "</div>"

    for index, item in enumerate(listings, start=1)

)


st.markdown(
    f"""
    <div class="listings-grid">
        {cards_html}
    </div>
    """,
    unsafe_allow_html=True,
)