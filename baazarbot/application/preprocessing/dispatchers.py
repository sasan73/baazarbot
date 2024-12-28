from typing import List

from beanie import Document

from baazarbot.infrastructure.db.mongo import start_mongo_client
from baazarbot.domain.base import VectorBaseDocument
from baazarbot.domain.types import DataCategory

from .chunking_data_handlers import (
    ChunkingArticleHandler,
    ChunkingDataHandler,
)
from .cleaning_data_handlers import (
    CleaningArticleHandler,
    CleaningDataHandler,
)
from .embedding_data_handlers import (
    EmbeddingArticleHandler,
    EmbeddingDataHandler,
)

class CleaningHandlerFactory():

    @staticmethod
    def create_handler(data_category: DataCategory) -> CleaningDataHandler:
        if data_category == DataCategory.ARTICLES:
            return CleaningArticleHandler()
        else:
            raise ValueError(f"{data_category} is an unsupported data type.")
    
class CleaningDispatcher():
    factory = CleaningHandlerFactory()
    
    @classmethod
    async def dispatch(cls, document: Document) -> VectorBaseDocument:
        data_category = document.name
        handler = cls.factory.create_handler(data_category)
        clean_model = handler.clean(document)
        
        logger.info(
            "Document cleaned successufully.",
            data_category=data_category,
            cleaned_content_len = len(clean_model.content),
        )
        return clean_model


class ChunkingHandlerFactory():
    @staticmethod
    def create_handler(data_category: DataCategory) -> ChunkingDataHandler:
        if data_category == DataCategory.ARTICLES:
            return ChunkingArticleHandler()
        else:
            raise ValueError("{data_category} is an unsupported data type.")

class ChunkingDispatcher():
    factory: ChunkingHandlerFactory()
    
    @classmethod
    def dispatch(cls, data_model: VectorBaseDocument) -> List[VectorBaseDocument]:
        data_category = data_model.get_category()
        handler = cls.factory.create_handler(data_category)
        chunk_models = handler.chunk(data_model)
        
        logger.info(
            "Document chunked successfully",
            data_category=data_category,
            num=len(chunk_models),
        )

        return chunk_models


class EmbeddingHandlerFactory:
    @staticmethod
    def create_handler(data_category: DataCategory) -> EmbeddingDataHandler:
        if data_category == DataCategory.ARTICLES:
            return EmbeddingArticleHandler()
        else:
            raise ValueError("{data_category} is an unsupported data type.")

class EmbeddingDispatcher():
    factory: EmbeddingHandlerFactory()
    
    @classmethod
    def dispatch(
        cls, data_model: VectorBaseDocument | List[VectorBaseDocument]
    ) -> VectorBaseDocument | List[VectorBaseDocument]:
        
        if not isinstance(data_model, list):
            data_model = [data_model]
        
        if len(data_model) == 0:
            return []

        data_category = data_model[0].get_category()
        assert all(
            data_model.get_category() == data_category for data_model in data_model
        ), "Data models must be of the same category."
        handler = cls.factory.create_handler(data_category)

        embedded_chunk_models = handler.embed_batch(data_model)
        
        if not isinstance(data_model, list):
            embedded_chunk_model = embedded_chunk_models[0]
        
        logger.info(
            "Data embedded successfully.",
            data_category=data_category,
        )

        return embedded_chunk_model
