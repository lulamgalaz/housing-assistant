import re
import json

from playwright.sync_api import sync_playwright

from scrapers.base_scraper import BaseScraper


class FotocasaScraper(BaseScraper):

    BASE_URL = "https://www.fotocasa.es"

    def __init__(
        self,
        city="barcelona",
        max_pages=1,
        headless=True,
    ):
        self.city = city
        self.max_pages = max_pages
        self.headless = headless


    def _build_url(self, page_number):

        url = (
            f"{self.BASE_URL}/es/alquiler/"
            f"viviendas/{self.city}-capital/"
            f"todas-las-zonas/l"
        )

        if page_number > 1:
            url += f"?page={page_number}"

        return url


    def _parse_price(self, text):

        if not text:
            return None

        match = re.search(
            r"[\d.,]+",
            text
        )

        if not match:
            return None

        raw = (
            match.group(0)
            .replace(".", "")
            .replace(",", "")
        )

        try:
            return int(raw)

        except ValueError:
            return None


    def scrape(self):

        listings = []

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=self.headless
            )

            page = browser.new_page()


            try:

                for page_number in range(
                    1,
                    self.max_pages + 1
                ):

                    url = self._build_url(
                        page_number
                    )


                    print(
                        f"Abriendo: {url}"
                    )


                    page.goto(
                        url,
                        wait_until="domcontentloaded",
                        timeout=30000,
                    )


                    # DEBUG

                    page.screenshot(
                        path="debug_fotocasa.png"
                    )


                    with open(
                        "debug_fotocasa.html",
                        "w",
                        encoding="utf-8",
                    ) as file:

                        file.write(
                            page.content()
                        )


                    scripts = page.query_selector_all(
                        'script[type="application/ld+json"]'
                    )


                    print(
                        f"JSON encontrados: {len(scripts)}"
                    )


                    for script in scripts:

                        try:

                            data = json.loads(
                                script.inner_text()
                            )


                            items = []


                            if isinstance(data, list):

                                items = data


                            elif isinstance(data, dict):

                                if "@graph" in data:

                                    items = data["@graph"]

                                else:

                                    items = [data]


                            for item in items:


                                item_type = item.get(
                                    "@type"
                                )


                                if item_type in [
                                    "Residence",
                                    "Product",
                                    "Apartment",
                                    "House",
                                ]:


                                    listing = {

                                        "source": "Fotocasa",

                                        "title": item.get(
                                            "name",
                                            "Sin título"
                                        ),

                                        "price": None,

                                        "neighborhood": "Barcelona",

                                        "district": None,

                                        "bedrooms": 0,

                                        "bathrooms": None,

                                        "surface_m2": None,

                                        "furnished": None,

                                        "available_from": None,


                                        "balcony": None,

                                        "terrace": None,

                                        "elevator": None,

                                        "air_conditioning": None,

                                        "separate_kitchen": None,

                                        "expenses_included": None,


                                        "contract_months": None,

                                        "contract_type": None,


                                        "floor": None,

                                        "exterior": None,


                                        "url": item.get(
                                            "url"
                                        ),

                                    }


                                    if listing["url"]:

                                        listings.append(
                                            listing
                                        )


                        except Exception:

                            pass


            except Exception as error:

                print(
                    f"Error durante scraping: {error}"
                )


            browser.close()


        return listings



if __name__ == "__main__":

    scraper = FotocasaScraper(
        city="barcelona",
        max_pages=1,
        headless=False,
    )


    results = scraper.scrape()


    print(
        f"Encontrados: {len(results)}"
    )


    for result in results[:5]:

        print(result)