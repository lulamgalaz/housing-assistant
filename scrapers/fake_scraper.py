from scrapers.base_scraper import BaseScraper


class FakeScraper(BaseScraper):

    def scrape(self):

        return [
            {
                "source": "Fake",
                "title": "Piso de prueba en Gràcia",
                "price": 1100,
                "neighborhood": "Gràcia",
                "bedrooms": 2,
                "url": "https://ejemplo.com/gracia",
            },
            {
                "source": "Fake",
                "title": "Departamento prueba Eixample",
                "price": 1200,
                "neighborhood": "Eixample",
                "bedrooms": 2,
                "url": "https://ejemplo.com/eixample",
            },
        ]