from abc import ABC, abstractmethod

from beanie import Document

class BaseCrawler(ABC):
    model: type[Document]

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None: ...


class BasePaginationCrawler(BaseCrawler, ABC):

    def _get_articles(self, url: str, start_page: int = 1, end_page: int = 3):
        articles = []
        for page_number in range(start_page, end_page+1):
            page_url = self._get_page_url(url, page_number)
            page_articles = self._get_page_article_urls(page_url)

            articles.extend(page_articles)

        return articles

    @abstractmethod
    def _get_page_article_urls(self, page_url: str) -> list[str]: ...

    @abstractmethod
    def _get_page_url(self, url, page_number: int) -> str: ...
