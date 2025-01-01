from loguru import logger
from qdrant_client.http import exceptions
from typing_extensions import Annotated
from zenml import step

from baazarbot.domain.cleaned_documents import CleanedDocument, CleanedArticleDocument

@step
def query_fe_store() -> Annotated[list[CleanedDocument], "queried_cleaned_documents"]:
    logger.info("Querying feature store.")

    articles = __fetch_articles()

    return articles


def __fetch_articles() -> list[CleanedArticleDocument]:
    return _fetch(CleanedArticleDocument)

def _fetch(document_class_type: CleanedDocument, limit: int = 1) -> CleanedDocument:

    try: 
        cleaned_documents, next_offset = document_class_type.bulk_find(limit=limit)
    except exceptions.UnexpectedResponse as e:
        logger.warning(f"Failed to fetch data from {document_class_type}. error message: {e}")
        return []

    while next_offset:
        documents, next_offset = document_class_type.bulk_find(limit=limit, offset=next_offset)
        cleaned_documents.extend(documents)

    return cleaned_documents
