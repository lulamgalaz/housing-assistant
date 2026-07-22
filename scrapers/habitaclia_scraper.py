from scrapers.browser_scraper import BrowserScraper

from bs4 import BeautifulSoup


class HabitacliaScraper(BrowserScraper):

    URL = (
        "https://www.habitaclia.com/"
        "viviendas-barcelona.htm"
    )


    def scrape(self):

        playwright, browser, page = self.get_page(
            self.URL
        )

        try:

            print(
                "TITLE:",
                page.title()
            )

            html = page.content()


            # -------------------------
            # Guardar HTML para analizar
            # -------------------------

            with open(
                "debug_habitaclia.html",
                "w",
                encoding="utf-8"
            ) as f:
                f.write(html)


            print(
                "HTML guardado: debug_habitaclia.html"
            )


            # -------------------------
            # Primer análisis básico
            # -------------------------

            soup = BeautifulSoup(
                html,
                "html.parser"
            )


            print(
                "Links encontrados:",
                len(soup.find_all("a"))
            )


            print(
                "Texto página:"
            )

            print(
                soup.get_text(
                    " ",
                    strip=True
                )[:1000]
            )


            return []


        finally:

            browser.close()
            playwright.stop()



if __name__ == "__main__":

    scraper = HabitacliaScraper()

    results = scraper.scrape()

    print(
        "Resultados:",
        len(results)
    )