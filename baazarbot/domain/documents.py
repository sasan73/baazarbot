from uuid import UUID, uuid4

from pydantic import Field
from beanie import Document

from baazarbot.domain.types import DataCategory

class ArticleDocument(Document):
    id: UUID = Field(default_factory=uuid4)
    name: str
    link: str
    content: dict
    platform: str

    class Settings:
        name = DataCategory.ARTICLES
