from loguru import logger
from zenml import step

from baazarbot.application import utils
from baazarbot.domain.base import VectorBaseDocument

@step
def load_vectordb(
    documents: Annotated[list, "documents"],
) -> Annotated[bool, "successful"]:
    logger.info(f"Loading {len(documents)} documents into the vector database.")
    
    grouped_documents = VectorBaseDocument.group_by_class(documetns)
    for document_class, document in grouped_documents.items():
        logger.info(f"Leading documents into {document_class.get_collection_name()}")
        for documents_batch in utilcs.misc.batch(documents, size=4):
            try:
                document_class.bulk_insert(document_batch)
            except Exception:
                logger.error(f"Failed to insert documents into {document_class.get_collection_name()}")

                return False

    return True
