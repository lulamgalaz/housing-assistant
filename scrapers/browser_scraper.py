from playwright.sync_api import sync_playwright


class BrowserScraper:

    def get_page(self, url):

        playwright = sync_playwright().start()

        browser = playwright.chromium.launch(
            headless=True
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 "
                "(Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 "
                "Chrome/125 Safari/537.36"
            )
        )

        page.goto(
            url,
            wait_until="networkidle",
            timeout=60000
        )

        return playwright, browser, page
        