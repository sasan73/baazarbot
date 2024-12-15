from zenml import pipeline

from steps import crawl_links

@pipeline
def digital_data_etl(links: list[str]) -> str:
    """ETL pipeline for digital data."""

    crawling_step = crawl_links(links=links)

    return crawling_step.invocation_id