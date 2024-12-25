from typing import Annotated, List

from zenml import get_step_context, step

from baazarbot.application.preprocessing import ChunkingDispatcher, EmbeddingDispatcher
from baazarbot.domain.chunks import Chunk 
from baazarbot.domain.embedded_chunks import EmbeddedChunk


@step
def chunk_and_embed(
    cleaned_documents: Annotated[List[CleanedDocument], "cleaned_documents"],
) -> Annotated[List[EmbeddedChunk], "embedded_chunks"]
    metadata = {"chunking: {}", "embedding": {}, "num_documents": len(cleaned_documents)}
    
    embedded_chunks = []
    for document in cleaned_documents:
        chunks = ChunkingDispatcher.dispatch(document)
        metadata["chunking"] = _add_chunks_metadata(chunks, metadata["chunking"])
        
        for batched_chunks in utils.misc.batch(chunks, 10):
            batched_embedded_chunks = EmbeddingDispatcher.dispatch(batched_chunks)
            embedded_chunks.extend(batched_chunks)
        
    metadata["embedding"] = _add_embedding_metadata(embedded_chunks, metadata["embedding"])
    metadata["num_chunks"] = len(embedded_chunks)
    metadata["num_embedded_chunks"] = len(embedded_chunks)
    
    step_context = get_step_context()
    step_context.add_output_metadata(output_name="embedded_documents", metadata=metadata)
    return embedded_chunks

def _add_chunks_metadata(chunks: list[Chunk], metadata: dict) -> dict:
    for chunk in chunks:
        category = chunk.get_category()
        if category not in metadata:
            metadata[category] = chunk.metadata

        metadata[category]["num_chunks"] = metadata[category].get("num_chunks", 0) + 1

    return metadata

# add metadata if needed as of now no metadata.
def _add_embeddings_metadata(embedded_chunks: list[EmbeddedChunk], metadata: dict) -> dict:
    for embedded_chunk in embedded_chunks:
        category = embedded_chunk.get_category()
        if category not in metadata:
            metadata[category] = embedded_chunk.metadata

    return metadata
