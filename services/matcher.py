from services.score import calculate_score


def matches_preferences(listing, preference):

    reasons = []


    # -------------------------
    # Filtros obligatorios
    # -------------------------

    if listing.price is None:
        return {
            "match": False,
            "score": 0,
            "reasons": ["Sin precio"]
        }


    if listing.price > preference.max_price:

        return {
            "match": False,
            "score": 0,
            "reasons": [
                "Precio superior al máximo"
            ]
        }


    if listing.bedrooms is None:

        return {
            "match": False,
            "score": 0,
            "reasons": [
                "Sin habitaciones"
            ]
        }


    if listing.bedrooms < preference.min_bedrooms:

        return {
            "match": False,
            "score": 0,
            "reasons": [
                "Menos habitaciones"
            ]
        }


    # -------------------------
    # Ranking
    # -------------------------

    score, reasons = calculate_score(
        listing,
        preference,
    )


    return {
        "match": True,
        "score": score,
        "reasons": reasons,
    }