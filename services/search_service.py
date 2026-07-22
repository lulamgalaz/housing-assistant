from scrapers.scraper_manager import ScraperManager
from services.listing_service import save_listings


def update_all_sources():
    """
    Ejecuta todos los scrapers disponibles,
    normaliza y guarda los anuncios encontrados.
    """

    manager = ScraperManager()

    result = manager.run_all()

    listings = result["listings"]

    if listings:
        save_listings(listings)

    return {
        "total": len(listings),
        "details": result["results"],
    }