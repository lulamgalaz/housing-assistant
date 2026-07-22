from config.neighborhoods import (
    PRIORITY_NEIGHBORHOODS,
    SECONDARY_NEIGHBORHOODS,
    AVOID_NEIGHBORHOODS,
)


def calculate_score(listing, preference):

    score = 0
    reasons = []


    # -------------------------
    # Precio
    # -------------------------

    if listing.price is not None:

        if listing.price <= preference.max_price:

            score += 30
            reasons.append(
                "💶 Dentro del presupuesto"
            )

        elif listing.price <= preference.max_price + 150:

            score += 15
            reasons.append(
                "💶 Apenas supera el presupuesto"
            )

        else:

            score -= 50
            reasons.append(
                "💸 Supera presupuesto"
            )


    # -------------------------
    # Habitaciones
    # -------------------------

    if listing.bedrooms is not None:

        if listing.bedrooms >= preference.min_bedrooms:

            score += 25
            reasons.append(
                "🛏 Habitaciones suficientes"
            )

        else:

            score -= 40
            reasons.append(
                "🛏 Menos habitaciones de las necesarias"
            )


    # -------------------------
    # Superficie
    # -------------------------

    if (
        preference.min_surface
        and listing.surface_m2
    ):

        if listing.surface_m2 >= preference.min_surface:

            score += 15
            reasons.append(
                "📐 Buena superficie"
            )

        else:

            score -= 10
            reasons.append(
                "📐 Superficie inferior"
            )


    # -------------------------
    # Barrio
    # -------------------------

    neighborhood = (
        listing.neighborhood
        or ""
    )


    if neighborhood in PRIORITY_NEIGHBORHOODS:

        score += 25
        reasons.append(
            "📍 Barrio prioritario"
        )


    elif neighborhood in SECONDARY_NEIGHBORHOODS:

        score += 15
        reasons.append(
            "📍 Barrio aceptable"
        )


    elif neighborhood in AVOID_NEIGHBORHOODS:

        score -= 100
        reasons.append(
            "🚫 Barrio descartado"
        )


    # -------------------------
    # Amueblado
    # -------------------------

    if listing.furnished:

        score += 10
        reasons.append(
            "🛋 Amueblado"
        )


    # -------------------------
    # Duración contrato
    # -------------------------

    if (
        preference.duration_months
        and listing.contract_months
    ):

        if listing.contract_months >= preference.duration_months:

            score += 10
            reasons.append(
                "📅 Duración compatible"
            )


    return score, reasons