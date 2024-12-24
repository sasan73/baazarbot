from beanie import Document

from baazarbot.domain.types import DataCategory

class ArticleDocument(Document):
    name: str
    link: str
    content: dict
    platform: str

    class Settings:
        name = DataCategory.ARTICLES
