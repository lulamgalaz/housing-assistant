import re
import time

import requests
from bs4 import BeautifulSoup

from scrapers.base_scraper import BaseScraper


class PisosScraper(BaseScraper):
    """
    Scraper para pisos.com (alquiler).

    pisos.com no tiene proteccion anti-bot y no usa JavaScript para renderizar
    el listado, por eso alcanza con requests + BeautifulSoup.

    Selectores verificados contra HTML real (2026-07): card, link, title,
    price, location, y las "chars" (habitaciones/banos/m2), que se
    identifican por texto ya que no tienen una clase distinta cada una.
    """

    BASE_URL = "https://www.pisos.com"

    SELECTORS = {
        "card": "div.ad-preview__info",
        "link": "a.ad-preview__title",
        "price": "span.ad-preview__price",
        "location": "p.ad-preview__subtitle",
        "chars": "p.ad-preview__char",
        "next_page": "div.pagination__next a",
    }

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        )
    }

    def __init__(self, city="barcelona_capital", max_pages=1, delay_seconds=2):
        self.city = city
        self.max_pages = max_pages
        self.delay_seconds = delay_seconds

    def _build_url(self):
        return f"{self.BASE_URL}/alquiler/pisos-{self.city}/"

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
        match = re.search(r"\d+", text)
        return int(match.group(0)) if match else None

    def _parse_card(self, card):
        link_el = card.select_one(self.SELECTORS["link"])
        if not link_el:
            return None

        href = link_el.get("href")
        if not href:
            return None
        if href.startswith("/"):
            href = self.BASE_URL + href

        title = link_el.get_text(strip=True)

        price_el = card.select_one(self.SELECTORS["price"])
        price = self._parse_price(price_el.get_text()) if price_el else None

        location_el = card.select_one(self.SELECTORS["location"])
        neighborhood = location_el.get_text(strip=True) if location_el else "N/A"

        bedrooms = None
        bathrooms = None
        surface_m2 = None

        for char_el in card.select(self.SELECTORS["chars"]):
            text = char_el.get_text(strip=True).lower()
            if "hab" in text and bedrooms is None:
                bedrooms = self._parse_int(text)
            elif "baño" in text and bathrooms is None:
                bathrooms = self._parse_int(text)
            elif "m²" in text or "m2" in text:
                surface_m2 = self._parse_int(text)

        return {
            "source": "Pisos.com",
            "title": title,
            "price": price,
            "neighborhood": neighborhood,
            "bedrooms": bedrooms or 0,
            "bathrooms": bathrooms,
            "surface_m2": surface_m2,
            "furnished": None,
            "available_from": None,
            "url": href,
        }

    def scrape(self):
        listings = []
        url = self._build_url()

        for page_number in range(1, self.max_pages + 1):
            response = requests.get(url, headers=self.HEADERS, timeout=15)

            if response.status_code != 200:
                print(f"Pagina {page_number}: status {response.status_code}, corto aca")
                break

            soup = BeautifulSoup(response.text, "html.parser")
            cards = soup.select(self.SELECTORS["card"])

            print(f"Pagina {page_number}: {len(cards)} tarjetas encontradas")

            if not cards:
                break

            for card in cards:
                listing = self._parse_card(card)
                if listing and listing["url"] and listing["price"]:
                    listings.append(listing)

            next_link = soup.select_one(self.SELECTORS["next_page"])
            if not next_link or not next_link.get("href"):
                break

            next_href = next_link["href"]
            url = next_href if next_href.startswith("http") else self.BASE_URL + next_href

            time.sleep(self.delay_seconds)

        return listings


if __name__ == "__main__":
    scraper = PisosScraper(city="barcelona_capital", max_pages=1)
    results = scraper.scrape()
    print(f"Encontrados: {len(results)}")
    for r in results[:5]:
        print(r)