from abc import ABC

from pydantic import UUID4, Field

from baazarbot.domain.types import DataCategory
from baazarbot.domain.base import VectorBaseDocument

class EmbeddedChunk(VectorBaseDocument, ABC):
    content: str
    embedding: list[float] | None
    platform: str
    document_id: UUID4
    metadata: dict = Field(default_factory=dict)

    @classmethod
    def to_context(cls, chunks: list["EmbeddedChunk"]) -> str:
        context = ""
        for i, chunk in enumerate(chunks):
            context += f"""
            Chunk {i + 1}:
            Type: {chunk.__class__.__name__}
            Platform: {chunk.platform}
            Content: {chunk.content}\n
            """

        return context


class EmbeddedArticleChunk(EmbeddedChunk):
    link: str

    class Config:
        name = "embedded_articles"
        category = DataCategory.ARTICLES
        use_vector_index = True
