from config.neighborhoods import (
    PRIORITY_NEIGHBORHOODS,
    SECONDARY_NEIGHBORHOODS,
    AVOID_NEIGHBORHOODS,
)


def calculate_score(listing, preference):

    score = 0
    reasons = []


    # -------------------------
    # Precio (30 puntos)
    # -------------------------

    if listing.price is not None:

        difference = (
            listing.price
            - preference.max_price
        )


        if difference <= 0:

            score += 30

            reasons.append(
                "💶 Dentro del presupuesto"
            )


        elif difference <= 100:

            score += 20

            reasons.append(
                "💶 Ligeramente superior al presupuesto"
            )


        elif difference <= 250:

            score += 10

            reasons.append(
                "💶 Algo superior al presupuesto"
            )


        else:

            reasons.append(
                "💸 Superior al presupuesto"
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

            score += 15

            reasons.append(
                "🛏 Falta una habitación"
            )


        else:

            score += 5

            reasons.append(
                "🛏 Menos habitaciones"
            )


    else:

        reasons.append(
            "🛏 Habitaciones sin datos"
        )



    # -------------------------
    # Superficie (20 puntos)
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

            score += 20

            reasons.append(
                "📐 Buena superficie"
            )


        elif difference >= -10:

            score += 12

            reasons.append(
                "📐 Superficie cercana"
            )


        else:

            score += 5

            reasons.append(
                "📐 Superficie inferior"
            )



    # -------------------------
    # Barrio (20 puntos)
    # -------------------------

    listing_neighborhood = (
        listing.neighborhood
        or ""
    )


    preferred_neighborhoods = []


    if preference.neighborhoods:

        preferred_neighborhoods = [
            n.strip()
            for n in preference.neighborhoods.split(",")
        ]



    if listing_neighborhood in preferred_neighborhoods:

        score += 30

        reasons.append(
            "📍 Barrio elegido"
        )


    elif listing_neighborhood in PRIORITY_NEIGHBORHOODS:

        score += 20

        reasons.append(
            "📍 Barrio prioritario"
        )


    elif listing_neighborhood in SECONDARY_NEIGHBORHOODS:

        score += 10

        reasons.append(
            "📍 Barrio aceptable"
        )


    elif listing_neighborhood in AVOID_NEIGHBORHOODS:

        score -= 20

        reasons.append(
            "🚫 Barrio evitado"
        )



    # -------------------------
    # Amueblado (5 puntos)
    # -------------------------

    if listing.furnished:

        score += 5

        reasons.append(
            "🛋 Amueblado"
        )



    # -------------------------
    # Duración contrato (5 puntos)
    # -------------------------

    if (
        preference.duration_months
        and listing.contract_months
    ):

        if (
            listing.contract_months
            >= preference.duration_months
        ):

            score += 5

            reasons.append(
                "📅 Duración compatible"
            )



    # -------------------------
    # Normalización final
    # -------------------------

    if score < 0:

        score = 0


    if score > 100:

        score = 100


    print(
    "SCORE DEBUG",
    listing.title,
    listing.price,
    listing.bedrooms,
    listing.surface_m2,
    listing.neighborhood,
    score,
    reasons
    )
    return score, reasons