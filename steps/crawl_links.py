from urllib.parse import urlparse
from loguru import logger

from tqdm import tqdm
from typing_extensions import Annotated
from zenml import get_step_context, step

from baazarbot.crawlers.dispatcher import CrawlerDispatcher

@step
def crawl_links(links: list[str]) -> Annotated[list[str], "crawled_links"]:
    """Crawl links"""

    dispatcher = dispatcher.build().register_ecoiran().regirster_iccima_reports().regirster_majlis_rules()

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
    crawler_domain = urlparse(link).netloc
    try:
        successful_crawls, total_crawls = dispatcher.extract(link)
        return successful_crawls, total_crawls, crawler_domain
    except Exception as e:
        logger.warning(f"Failed to crawl link: {link}. Error: {e}")
        return 0, crawler_domain

def _add_metadata(metadata: dict, crawler_domain: str, successful_crawls: int, total_crawls: int) -> None:
    """Add the number of successful crawls to the metadata."""
    
    if crawler_domain not in metadata:
        metadata[crawler_domain] = 0
    metadata[crawler_domain]["successful_crawls"] = metadata.get("successful_crawls", 0) + successful_crawls
    metadata[crawler_domain]["total_crawls"] = metadata.get("total_crawls", 0) + total_crawls

    return metadata
