# from concurrent.futures import ThreadPoolExecutor, as_completed 
from loguru import logger 
from typing import Annotated
import asyncio

from zenml import get_step_context, step

from baazarbot.domain.documents import ArticleDocument
from baazarbot.infrastructure.db.mongo import start_mongo_client

@step
def get_data_warehouse() -> Annotated[list, "raw_documents"]:    
    documents = fetch_all_data()
    
    step_context = get_step_context()
    step_context.add_output_metadata(output_name="raw_documents", metadata=_get_metadata(documents))
    return documents

def fetch_all_data():
    """fetch data from multiple data classes e.g. ArticleDocuments etc."""
    # When new datatypes are added this process we can use use multitasking
    articles = asyncio.run(__fetch_articles())
    return articles

async def __fetch_articles():
    """fetch ArticleDocument data from mongoDB."""
    await start_mongo_client()
    return await ArticleDocument.find_all().to_list()

def _get_metadata(documents: list) -> dict:
    metadata = {
        "num_documents": len(documents)
    }
    dates = []
    for document in documents:
        collection_name = document.name
        if collection_name not in metadata:
            metadata[collection_name] = {}

        metadata[collection_name]["num_documents"] = metadata[collection_name].get("num_documents", 0) + 1
        dates.append(document.content["DateTime"])

    metadata[collection_name]["start_date"] = min(dates).isoformat()
    metadata[collection_name]["end_date"] = max(dates).isoformat()

    return metadata
