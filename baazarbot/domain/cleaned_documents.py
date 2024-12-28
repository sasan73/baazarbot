from abc import ABC
from datetime import datetime

from baazarbot.domain.types import DataCategory
from baazarbot.domain.base import VectorBaseDocument

class CleanedDocument(VectorBaseDocument, ABC):
    content: str
    platform: str

class CleanedArticleDocument(CleanedDocument):
    link: str
    date_created: datetime

    class Config:
        name = "cleaned_articles"
        category = DataCategory.ARTICLES
        use_vector_index = False
