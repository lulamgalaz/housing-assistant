from scrapers.pisos_scraper import PisosScraper


class ScraperManager:
    """
    Coordina la ejecución de múltiples scrapers.

    Cada scraper debe devolver una lista de diccionarios
    con el formato esperado por el normalizador.
    """

    def __init__(self):
        self.scrapers = [
            PisosScraper(
                city="barcelona_capital",
                max_pages=2,
            ),
        ]

    def run_all(self):
        """
        Ejecuta todos los scrapers disponibles.

        Si un scraper falla, no interrumpe los demás.
        """

        all_listings = []
        results = []

        for scraper in self.scrapers:

            scraper_name = scraper.__class__.__name__

            try:
                listings = scraper.scrape()

                all_listings.extend(listings)

                results.append(
                    {
                        "scraper": scraper_name,
                        "status": "success",
                        "count": len(listings),
                    }
                )

            except Exception as error:

                results.append(
                    {
                        "scraper": scraper_name,
                        "status": "error",
                        "count": 0,
                        "error": str(error),
                    }
                )

        return {
            "listings": all_listings,
            "results": results,
        }