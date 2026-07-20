from abc import ABC, abstractmethod


class BaseScraper(ABC):

    @abstractmethod
    def scrape(self):
        """
        Devuelve una lista de anuncios.
        """
        pass