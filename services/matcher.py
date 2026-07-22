print("MATCHER CARGADO")
from services.score import calculate_score


def matches_preferences(listing, preference):

    score, reasons = calculate_score(
        listing,
        preference,
    )

    return {
        "match": score >= 50,
        "score": score,
        "reasons": reasons,
    }