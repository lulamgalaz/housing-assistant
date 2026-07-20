from scrapers.base_scraper import BaseScraper


class FakeScraper(BaseScraper):

    def scrape(self):

        return [
            {
                "source": "Habitaclia",
                "title": "Piso luminoso cerca de Passeig de Sant Joan",
                "price": 1150,
                "neighborhood": "Eixample",
                "bedrooms": 2,
                "bathrooms": 1,
                "surface_m2": 65,
                "furnished": True,
                "available_from": "2026-09-01",
                "url": "https://ejemplo.com/eixample",
            },
            {
                "source": "Habitaclia",
                "title": "Departamento tranquilo en Gràcia",
                "price": 1500,
                "neighborhood": "Gràcia",
                "bedrooms": 2,
                "bathrooms": 1,
                "surface_m2": 55,
                "furnished": False,
                "available_from": "2026-09-01",
                "url": "https://ejemplo.com/gracia",
            },
        ]