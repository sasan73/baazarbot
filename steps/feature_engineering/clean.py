from loguru import logger
from typing import List
from beanie import Document

from zenml import get_step_context, step

from baazarbot.domain.cleaned_documents import CleanedDocument

@step
def clean_documents(
    documents: Annotated[List[Document], "raw_documents"],
) -> Annotated[List[CleanedDocument], "cleaned_documents"]:
    cleaned_documents = []
    for document in documents:
        cleaned_document = CleaningDispatcher.dispatch(document)
        cleaned_documents.append(cleaned_document)
    
    step_context = get_step_context()
    step_context.add_output_metadata(output_name="cleaned_documents", metadata=_get_metadata(cleaned_documents))
    return cleaned_documents

def _get_metadata(documents: List[CleanedDocument]) -> dict:
    metadata = {
        "num_documents": len(documents),
    }
    for document in documetns:
        category = document.get_category()
        if category not in metadata:
            metadata[category] = {}
        
        metadata[category]["num_documents"] = metadata[category].get("num_documents", 0) + 1

    return metadata
