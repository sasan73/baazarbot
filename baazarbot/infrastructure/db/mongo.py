from loguru import logger
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from baazarbot.settings import settings
from baazarbot.domain.documents import ArticleDocument

async def start_mongo_client():
    # Create Motor client
    client = AsyncIOMotorClient(settings.DATABASE_HOST)

    # Init beanie with the Product document class
    await init_beanie(database=client.baazarbot, document_models=[ArticleDocument])
