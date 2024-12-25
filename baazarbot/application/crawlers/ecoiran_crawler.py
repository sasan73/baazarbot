from datetime import datetime
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import time
from loguru import logger

from baazarbot.application.crawlers.base import BasePaginationCrawler
from baazarbot.domain.types import DataCategory
from baazarbot.domain.documents import ArticleDocument
from baazarbot.infrastructure.db.mongo import start_mongo_client


class EcoiranCrawler(BasePaginationCrawler):
    model = ArticleDocument

    def __init__(self, base_url):
        super().__init__()
        self.BASE_URL = base_url        


    async def extract(self, link: str, **kwargs) -> None:
        await start_mongo_client()
        logger.info("Started mongoDB client!")
        instances = []
        articles = self._get_articles(link)
        total_crawls = len(articles)
        for article_instance, article_link in enumerate(articles):
            # sleep for one second as to not overload the website
            if article_instance % 10 == 0:
                time.sleep(1)
            # check if articles are already added to the database
            old_model = await self.model.find(self.model.link == article_link).to_list()
            if len(old_model) > 0:
                logger.info(f"Article already exists in the database: {article_link}")
                continue
            # if crawling was not successful skip.
            # try:
            header, date_obj, description, content_str = self._get_content_sections(article_link)
            content = {
                "Header": header,
                "DateTime": date_obj,
                "Content Description": description,
                "Content": content_str,
            }
            # except Exception as e:
            #     logger.warning(f"Failed to crawl link: {article_link}. Error: {e}")
            #     continue

            parsed_url = urlparse(self.BASE_URL)
            platform = parsed_url.netloc

            instance = self.model(
                name=DataCategory.ARTICLES,
                content=content,
                platform=platform,
                link=article_link
            )
            instances.append(instance)

        successful_crawls = len(instances)
        await self.model.insert_many(instances)
        return successful_crawls, total_crawls


    def _get_page_article_urls(self, page_url: str) -> list[str]:
        page_articles = []
        response = requests.get(page_url)
        page_soup = BeautifulSoup(response.text, "html.parser")

        # Find all article links on the page
        page_soup_latest_articles = page_soup.find("div", class_="service_Section02_Row01_Column01")
        for article_soup in page_soup_latest_articles.find_all("a", class_="res ap-ratio"):
            article = self.BASE_URL + article_soup.get("href")
            page_articles.append(article)
        return page_articles


    def _get_page_url(self, url, page_number: int) -> str:
        return f"{url}?page={page_number}"


    def _get_content_sections(self, article_link: str) -> tuple:
        
        response = requests.get(article_link)
        soup = BeautifulSoup(response.text, "html.parser")
        # get article header
        header = soup.find("div", class_="contentTitle").h1.string
        # get article title 
        date_str = soup.find("time", class_="news-time").get("datetime")
        date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
        # get content description
        description = soup.find("div", class_="contentDescription").p.string
        # get article content
        content_body = soup.find("div", class_="contentBody")
        content_list = content_body.find_all("p", recursive=False)
        content_list_string = [content_html.string for content_html in content_list]
        content = "\n\n".join([content_string for content_string in content_list_string if content_string is not None])
        return header, date_obj, description, content
