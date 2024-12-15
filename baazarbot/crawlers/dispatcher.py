import re
from urllib.parse import urlparse

from loguru import logger

from baazarbot.application.crawlers.base import BaseCrawler
from baazarbot.application.crawlers.ecoiran import EcoiranCrawler
from baazarbot.application.crawlers.majlis_rules import MajlisRulesCrawler
from baazarbot.application.crawlers.iccima_reports import ICCIMAReportsCrawler
from baazarbot.application.crawlers.custom_article import CustomArticleCrawler

class CrawlerDispatcher:
    """Abstract base class for a dispatcher."""
    def __init__(self):
        """"Initialize the dispatcher."""
        self._crawlers = {}
        

    @classmethod
    def build(cls):
        """Build the dispatcher object."""
        dispatcher = cls()

        return dispatcher
    
    def register_ecoiran(self):
        """Register the Ecoiran crawler"""
        url = "ecoiran.com"
        crawler = EcoiranCrawler(url)
        register(url, crawler)

        return self
        
    def regirster_majlis_rules(self):
        url = "rc.majlis.ir"
        crawler = MajlisRulesCrawler()
        register(url, crawler)

        return self

    def regirster_iccima_reports(self):
        url = "iccima.ir"
        crawler = MajlisRulesCrawler()
        register(url, crawler)

        return self

    def register(url: str, crawler: BaseCrawler):
        """Register a new domain."""
        domain = urlparse(url).netloc

        self._crawlers[r"https:://(www.)?{}/*".format(re.escape(domain))] = crawler
    
    def get_crawler(self, url: str) -> BaseCrawler:
        """Get the crawler for the given domain."""
        
        for pattern, crawler in self._crawlers.items():
            if re.match(pattern, url):
                return crawler
            
            else:
                logger.warning(f"No crawler found for {url}. Defaulting to CustomArticleCrawler.")
                
                return CustomArticleCrawler()
