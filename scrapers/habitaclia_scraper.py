import re

from playwright.sync_api import sync_playwright

from scrapers.base_scraper import BaseScraper


class HabitacliaScraper(BaseScraper):
    """
    Scraper para habitaclia.com (alquiler de pisos).

    IMPORTANTE: los selectores CSS de abajo (SELECTORS) están basados en la
    estructura pública del listado de resultados, pero el sitio puede cambiar
    su HTML en cualquier momento. Si el scraper deja de traer resultados (o
    trae datos vacíos), lo primero a revisar es este diccionario: abrí la
    página de resultados en el navegador, inspeccioná una tarjeta de anuncio
    (clic derecho > Inspeccionar) y actualizá el selector que corresponda.
    """

    BASE_URL = "https://www.habitaclia.com"

    SELECTORS = {
        "card": "article",  # contenedor de cada anuncio en el listado
        "link": "a[href*='/alquiler-']",
        "price": "[class*='price']",
        "title": "[class*='title']",
        "location": "[class*='location'], [class*='zone']",
        "features": "[class*='feature'] li, ul li",
        "cookie_accept": "#onetrust-accept-btn-handler",
    }

    def __init__(self, city="barcelona", max_pages=1, headless=True):
        self.city = city
        self.max_pages = max_pages
        self.headless = headless

    def _build_url(self, page_number):
        slug = f"alquiler-pisos-{self.city}"
        if page_number == 1:
            return f"{self.BASE_URL}/{slug}.htm"
        return f"{self.BASE_URL}/{slug}-{page_number}.htm"

    def _accept_cookies(self, page):
        try:
            page.click(self.SELECTORS["cookie_accept"], timeout=3000)
        except Exception:
            pass

    def _parse_price(self, text):
        if not text:
            return None
        match = re.search(r"[\d.,]+", text)
        if not match:
            return None
        raw = match.group(0).replace(".", "").replace(",", "")
        try:
            return int(raw)
        except ValueError:
            return None

    def _parse_int(self, text):
        if not text:
            return None
        match = re.search(r"\d+", text)
        return int(match.group(0)) if match else None

    def _parse_card(self, card):
        link_el = card.query_selector(self.SELECTORS["link"])
        if not link_el:
            return None

        href = link_el.get_attribute("href")
        if not href:
            return None
        if href.startswith("/"):
            href = self.BASE_URL + href

        title_el = card.query_selector(self.SELECTORS["title"])
        price_el = card.query_selector(self.SELECTORS["price"])
        location_el = card.query_selector(self.SELECTORS["location"])
        feature_els = card.query_selector_all(self.SELECTORS["features"])

        features_text = [el.inner_text() for el in feature_els if el.inner_text()]

        bedrooms = None
        bathrooms = None
        surface_m2 = None
        for feature in features_text:
            lowered = feature.lower()
            if "hab" in lowered and bedrooms is None:
                bedrooms = self._parse_int(feature)
            elif "bañ" in lowered and bathrooms is None:
                bathrooms = self._parse_int(feature)
            elif ("m2" in lowered or "m²" in lowered) and surface_m2 is None:
                surface_m2 = self._parse_int(feature)

        price = self._parse_price(price_el.inner_text()) if price_el else None

        return {
            "source": "Habitaclia",
            "title": title_el.inner_text().strip() if title_el else "Sin título",
            "price": price,
            "neighborhood": location_el.inner_text().strip() if location_el else "N/A",
            "bedrooms": bedrooms or 0,
            "bathrooms": bathrooms,
            "surface_m2": surface_m2,
            "furnished": None,
            "available_from": None,
            "url": href,
        }

    def scrape(self):
        listings = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            page = browser.new_page()

            try:
                for page_number in range(1, self.max_pages + 1):
                    url = self._build_url(page_number)
                    page.goto(url, wait_until="domcontentloaded")

                    if page_number == 1:
                        self._accept_cookies(page)

                    try:
                        page.wait_for_selector(self.SELECTORS["card"], timeout=10000)
                    except Exception:
                        break

                    cards = page.query_selector_all(self.SELECTORS["card"])

                    for card in cards:
                        listing = self._parse_card(card)
                        if listing and listing["url"] and listing["price"]:
                            listings.append(listing)
            except Exception as error:
                print(f"Error durante el scraping: {error}")
                try:
                    page.screenshot(path="debug_habitaclia.png")
                    print("Captura guardada en debug_habitaclia.png")
                except Exception:
                    print("No se pudo guardar la captura (el navegador ya estaba cerrado)")

            browser.close()

        return listings


if __name__ == "__main__":
    scraper = HabitacliaScraper(city="barcelona", max_pages=1, headless=False)
    results = scraper.scrape()
    print(f"Encontrados: {len(results)}")
    for r in results[:5]:
        print(r)
