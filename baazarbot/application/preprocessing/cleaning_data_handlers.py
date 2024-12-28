from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from beanie import Document

from baazarbot.domain.documents import ArticleDocument
from baazarbot.domain.cleaned_documents import CleanedDocument, CleanedArticleDocument
from baazarbot.application.preprocessing.operations import clean_text

DocumentT = TypeVar("DocumentT", bound=Document)
CleanedDocumentT = TypeVar("CleanedDocumentT", bound=CleanedDocument)

class CleaningDataHandler(ABC, Generic[DocumentT, CleanedDocumentT]):
    
    @abstractmethod
    def clean(self, data_model: DocumentT) -> CleanedDocumentT:
        pass

class CleaningArticleHandler(CleaningDataHandler):

    def clean(self, data_model: ArticleDocument) -> CleanedArticleDocument:

        contents = data_model.content
        valid_article_content = contents["Header"]
        valid_article_content += " #### " + contents["Content Description"]
        valid_article_content += " #### " + contents["Content"]

        return CleanedArticleDocument(
            id=data_model.id,
            content=clean_text(valid_article_content),
            date_created=data_model.content["DateTime"],
            platform=data_model.platform,
            link=data_model.link,
        )
