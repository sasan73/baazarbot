from abc import ABC

from pydantic import UUID4, Field

from baazarbot.domain.types import DataCategory
from baazarbot.domain.base import VectorBaseDocument

class Chunk(VectorBaseDocument, ABC):
    content: str
    platform: str
    document_id: UUID4
    metadata: dict = Field(default_factory=dict)

class ArticleChunk(Chunk):
    link: str

    class Config:
        category = DataCategory.ARTICLES
