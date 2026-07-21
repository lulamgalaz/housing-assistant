import re


def normalize_listing(listing: dict) -> dict:
    """
    Recibe un anuncio de cualquier scraper y devuelve
    un anuncio con datos normalizados.
    """

    normalized = listing.copy()

    normalized["neighborhood"] = normalize_neighborhood(
        listing.get("neighborhood")
    )

    normalized["district"] = extract_district(
        listing.get("neighborhood")
    )

    return normalized


def normalize_neighborhood(text):

    if not text:
        return None

    return text.split("(")[0].strip()


def extract_district(text):

    if not text:
        return None

    match = re.search(
        r"Distrito (.*?)\.",
        text
    )

    if match:
        return match.group(1).strip()

    return None