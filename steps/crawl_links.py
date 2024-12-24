from urllib.parse import urlparse
from loguru import logger
import asyncio

from tqdm import tqdm
from typing_extensions import Annotated
from zenml import get_step_context, step

from baazarbot.application.crawlers.dispatcher import CrawlerDispatcher

@step
def crawl_links(links: list[str]) -> Annotated[list[str], "crawled_links"]:
    """Crawl links"""

    dispatcher = CrawlerDispatcher.build().register_ecoiran()

    metadata = {}
    successful_crawls_total = 0
    total_links = 0
    for link in tqdm(links):
        successful_crawls, crawler_domain, total_crawls = _crawl_link(dispatcher, link)

        successful_crawls_total += successful_crawls
        total_links += total_crawls
        metadata = _add_metadata(metadata, crawler_domain, successful_crawls, total_crawls)
    
    step_context = get_step_context()
    step_context.add_output_metadata(output_name="crawled_links", metadata=metadata)

    logger.info(f"Successfully crawled {successful_crawls_total} outof a total of {total_links} links.")    
    return links


def _crawl_link(dispatcher: CrawlerDispatcher, link: str) -> tuple:
    """Crawl a single link and return the number of successful crawls and the crawled domain."""
    crawler = dispatcher.get_crawler(link)
    crawler_domain = urlparse(link).netloc
    try:
        successful_crawls, total_crawls = asyncio.run(crawler.extract(link))
        return successful_crawls, crawler_domain, total_crawls
    except Exception as e:
        logger.warning(f"Failed to crawl link: {link}. Error: {e}")
        return 0, crawler_domain, 0

def _add_metadata(metadata: dict, crawler_domain: str, successful_crawls: int, total_crawls: int) -> None:
    """Add the number of successful crawls to the metadata."""
    
    if crawler_domain not in metadata:
        metadata[crawler_domain] = {}
    metadata[crawler_domain]["successful_crawls"] = metadata.get(crawler_domain, {}).get("successful_crawls", 0) + successful_crawls
    metadata[crawler_domain]["total_crawls"] = metadata.get(crawler_domain, {}).get("total_crawls", 0) + total_crawls

    return metadata
