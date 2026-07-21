from config.profile import (
    PRIORITY_NEIGHBORHOODS,
    SECONDARY_NEIGHBORHOODS,
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
            reasons.append("💶 Dentro del presupuesto")

        elif listing.price <= preference.max_price + 150:
            score += 15
            reasons.append("💶 Apenas supera el presupuesto")

    # -------------------------
    # Habitaciones
    # -------------------------

    if listing.bedrooms is not None:

        if listing.bedrooms >= preference.min_bedrooms:
            score += 20
            reasons.append("🛏 Habitaciones suficientes")

    # -------------------------
    # Barrio
    # -------------------------

    neighborhood = listing.neighborhood or ""

    if neighborhood in PRIORITY_NEIGHBORHOODS:

        score += 25
        reasons.append("📍 Barrio prioritario")

    elif neighborhood in SECONDARY_NEIGHBORHOODS:

        score += 15
        reasons.append("📍 Barrio aceptable")

    # -------------------------
    # Amueblado
    # -------------------------

    if listing.furnished:

        score += 10
        reasons.append("🛋 Amueblado")

    # -------------------------
    # Superficie
    # -------------------------

    if listing.surface_m2:

        if listing.surface_m2 >= 60:
            score += 15
            reasons.append("📐 Buena superficie")

        elif listing.surface_m2 >= 45:
            score += 8
            reasons.append("📐 Superficie aceptable")

    return score, reasons