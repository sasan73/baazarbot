from typing import Annotated

from loguru import logger
from zenml import step

from baazarbot.application import utils
from baazarbot.domain.base import VectorBaseDocument

@step
def load_to_vector_db(
    documents: Annotated[list, "documents"],
) -> Annotated[bool, "successful"]:
    logger.info(f"Loading {len(documents)} documents into the vector database.")
    
    grouped_documents = VectorBaseDocument.group_by_class(documents)
    for document_class, document in grouped_documents.items():
        logger.info(f"Loading documents into {document_class.get_collection_name()}")
        for documents_batch in utils.misc.batch(documents, size=4):
            try:
                document_class.bulk_insert(documents_batch)
            except Exception as e:
                logger.error(f"Failed to insert documents into {document_class.get_collection_name()} due to {e}")

                return False

    return True
