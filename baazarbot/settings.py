from pydantic_settings import BaseSettings, SettingsConfigDict
from loguru import logger

from zenml.client import Client

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # OpenAI API
    OPENAI_MODEL_ID: str = "gpt-4o-mini"
    OPENAI_API_KEY: str | None = None

    # Huggingface API
    HUGGINGFACEHUB_API_TOKEN: str | None = None

    # Comet ML (during training)
    COMET_API_KEY: str | None = None
    COMET_PROJECT: str = "baazarbot"

    # --- Required settings when deploying the code. ---
    # --- Otherwise, default values values work fine. ---

    # MongoDB database
    DATABASE_HOST: str = "mongodb://baazarbot:baazarbot@127.0.0.1:27017"
    DATABASE_NAME: str = "baazarbot"

    # Qdrant vector database
    USE_QDRANT_CLOUD: bool = False
    QDRANT_DATABASE_HOST: str = "localhost"
    QDRANT_DATABASE_PORT: int = 6333
    QDRANT_CLOUD_URL: str = "str"
    QDRANT_APIKEY: str | None = None

    # RAG
    TEXT_EMBEDDING_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_MODEL_DEVICE: str = "cpu"

    # DATASET Generation
    DATASET_GENERATION_MODEL_ID: str = "meta-llama/Llama-3.1-8B-Instruct"

    # @classmethod
    # def load_settings(cls) -> "Settings":
    #     """
    #     Tries to load the settings from the ZenML secret store. If the secret does not exist, it initializes the settings from the .env file and default values.

    #     Returns:
    #         Settings: The initialized settings object.
    #     """

    #     try:
    #         logger.info("Loading settings from the ZenML secret store.")

    #         settings_secrets = Client().get_secret("settings")
    #         settings = Settings(**settings_secrets.secret_values)
    #     except (RuntimeError, KeyError):
    #         logger.warning(
    #             "Failed to load settings from the ZenML secret store. Defaulting to loading the settings from the '.env' file."
    #         )
    #         settings = Settings()

    #     return settings

settings = Settings()
