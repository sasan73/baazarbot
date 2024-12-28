import hashlib
from uuid import UUID
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from baazarbot.application.preprocessing.operations import chunk_text
from baazarbot.domain.cleaned_documents import CleanedDocument, CleanedArticleDocument
from baazarbot.domain.chunks import Chunk, ArticleChunk

CleanedDocumentT = TypeVar("CleanedDocumentT" , bound=CleanedDocument)
ChunkT = TypeVar("ChunkT", bound=Chunk)

class ChunkingDataHandler(ABC, Generic[CleanedDocumentT, ChunkT]):
    
    @abstractmethod
    def chunk(self, data_model: CleanedDocumentT) -> list[ChunkT]:
        pass
    

class ChunkingArticleHandler(ChunkingDataHandler):
    @property
    def metadata(self) -> dict:
        return {
            "chunk_size": 500,
            "chunk_overlap": 20,
        }
    
    def chunk(self, data_model: CleanedArticleDocument) -> list[ArticleChunk]:
        chunked_text = chunk_text(data_model.content, chunk_size=self.metadata["chunk_size"], chunk_overlap=self.metadata["chunk_overlap"])

        chunks = []
        for chunk in chunked_text:
            chunk_id = hashlib.md5(chunk.encode()).hexdigest()
            chunks.append(
                ArticleChunk(
                    id=UUID(chunk_id, version=4),
                    document_id=data_model.id,
                    content=chunk,
                    platform=data_model.platform,
                    link=data_model.link,
                    metadata=self.metadata,
                )
            )

        return chunks
