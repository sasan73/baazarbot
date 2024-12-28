from abc import ABC, abstractmethod
from typing import TypeVar, Generic, cast

from baazarbot.domain.chunks import Chunk, ArticleChunk
from baazarbot.domain.embedded_chunks import EmbeddedChunk, EmbeddedArticleChunk
from baazarbot.application.networks import EmbeddingModelSingleton

ChunkT = TypeVar("ChunkT", bound=Chunk)
EmbeddedChunkT = TypeVar("EmbeddedChunkT", bound=EmbeddedChunk)

embedding_model = EmbeddingModelSingleton()

class EmbeddingDataHandler(ABC, Generic[ChunkT, EmbeddedChunkT]):

    def embed(self, data_model: ChunkT) -> EmbeddedChunkT:
        return self.embed_batch([data_model])[0]
    
    def embed_batch(self, data_model: list[ChunkT]) -> list[EmbeddedChunkT]:
        embedding_model_input = [data_model.content for data_model in data_model]
        embeddings = embedding_model(embedding_model_input)
        
        embedded_chunk = [
            self.map_chunks(data_model, cast(list[float], embedding)) 
            for data_model, embedding in zip(data_model, embeddings, strict=False)
        ]
        return embedded_chunk
    
    @abstractmethod
    def map_chunks(self, data_model: ChunkT, embedding: list[float]) -> EmbeddedChunkT:
        pass

class EmbeddingArticleHandler(EmbeddingDataHandler):
    
    def map_chunks(self, data_model: ArticleChunk, embedding: list[float]) -> EmbeddedArticleChunk:
        return EmbeddedArticleChunk(
            id=data_model.id,
            content=data_model.content,
            embedding=embedding,
            platform=data_model.platform,
            document_id=data_model.document_id,
            link=data_model.link,
            metadata={
                "embedding_model_id": embedding_model.model_id,
                "embedding_size": embedding_model.embedding_size,
                "max_input_length": embedding_model.max_input_length,
            },
        )
