from config.neighborhoods import (
    PRIORITY_NEIGHBORHOODS,
    SECONDARY_NEIGHBORHOODS,
    AVOID_NEIGHBORHOODS,
)


def calculate_score(listing, preference):

    score = 0
    reasons = []


    # -------------------------
    # Precio (40 puntos)
    # -------------------------

    if listing.price is not None:

        difference = (
            listing.price
            - preference.max_price
        )


        if difference <= 0:

            score += 40

            reasons.append(
                "💶 Dentro del presupuesto"
            )


        elif difference <= 100:

            score += 25

            reasons.append(
                "💶 Hasta 100€ sobre presupuesto"
            )


        elif difference <= 250:

            score += 10

            reasons.append(
                "💶 Algo superior al presupuesto"
            )


        else:

            score -= 20

            reasons.append(
                "💸 Muy superior al presupuesto"
            )


    else:

        reasons.append(
            "💸 Precio no informado"
        )



    # -------------------------
    # Habitaciones (25 puntos)
    # -------------------------

    if listing.bedrooms is not None:


        if listing.bedrooms >= preference.min_bedrooms:

            score += 25

            reasons.append(
                "🛏 Habitaciones suficientes"
            )


        elif (
            preference.min_bedrooms
            - listing.bedrooms
            == 1
        ):

            score += 10

            reasons.append(
                "🛏 Falta una habitación"
            )


        else:

            reasons.append(
                "🛏 Menos habitaciones"
            )



    # -------------------------
    # Superficie (15 puntos)
    # -------------------------

    if (
        preference.min_surface
        and listing.surface_m2
    ):


        difference = (
            listing.surface_m2
            - preference.min_surface
        )


        if difference >= 0:

            score += 15

            reasons.append(
                "📐 Buena superficie"
            )


        elif difference >= -10:

            score += 8

            reasons.append(
                "📐 Superficie cercana"
            )


        else:

            reasons.append(
                "📐 Superficie inferior"
            )



    # -------------------------
    # Barrio (20 puntos)
    # -------------------------

    neighborhood = (
        listing.neighborhood
        or ""
    )


    preferred_neighborhoods = []


    if preference.neighborhoods:

        preferred_neighborhoods = [
            n.strip()
            for n in preference.neighborhoods.split(",")
        ]


    if neighborhood in preferred_neighborhoods:

        score += 20

        reasons.append(
            "📍 Barrio elegido"
        )


    elif neighborhood in PRIORITY_NEIGHBORHOODS:

        score += 15

        reasons.append(
            "📍 Barrio prioritario"
        )


    elif neighborhood in SECONDARY_NEIGHBORHOODS:

        score += 8

        reasons.append(
            "📍 Barrio aceptable"
        )


    elif neighborhood in AVOID_NEIGHBORHOODS:

        score -= 30

        reasons.append(
            "🚫 Barrio evitado"
        )



    # -------------------------
    # Extras vivienda
    # -------------------------

    if listing.furnished:

        score += 5

        reasons.append(
            "🛋 Amueblado"
        )


    if listing.balcony:

        score += 5

        reasons.append(
            "🌿 Balcón"
        )


    if listing.terrace:

        score += 8

        reasons.append(
            "🌞 Terraza"
        )


    if listing.elevator:

        score += 3

        reasons.append(
            "🛗 Ascensor"
        )



    # -------------------------
    # Contrato
    # -------------------------

    if (
        preference.duration_months
        and listing.contract_months
    ):

        if listing.contract_months >= preference.duration_months:

            score += 5

            reasons.append(
                "📅 Duración compatible"
            )



    # -------------------------
    # Limites
    # -------------------------

    if score < 0:
        score = 0


    if score > 100:
        score = 100


    return score, reasons