"""MongoDB connection manager using Motor async driver."""

from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.config import Settings


class MongoDBConnectionManager:
    """
    Manages MongoDB connection lifecycle with connection pooling.
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client: AsyncIOMotorClient | None = None
        self._database: AsyncIOMotorDatabase | None = None

    @property
    def client(self) -> AsyncIOMotorClient | None:
        return self._client

    @property
    def database(self) -> AsyncIOMotorDatabase | None:
        return self._database

    async def connect(self) -> None:
        """Establish connection and configure connection pool."""
        url = self._settings.mongodb_url
        if not url:
            return

        self._client = AsyncIOMotorClient(
            url,
            maxPoolSize=self._settings.mongodb_max_pool_size,
            minPoolSize=self._settings.mongodb_min_pool_size,
            maxIdleTimeMS=self._settings.mongodb_max_idle_time_ms,
            serverSelectionTimeoutMS=self._settings.mongodb_server_selection_timeout_ms,
            uuidRepresentation="standard",
        )
        self._database = self._client[self._settings.mongodb_database_name]

        # Verify connection (triggers actual connect and raises if unreachable)
        await self._client.admin.command("ping")

    async def close(self) -> None:
        """Close the client and release connection pool."""
        if self._client is not None:
            self._client.close()
            self._client = None
            self._database = None


async def get_database(request: Request) -> AsyncIOMotorDatabase | None:
    """
    Dependency that returns the MongoDB database instance.
    Returns None if MongoDB is not configured (mongodb_url not set).
    """
    return getattr(request.app.state, "mongodb_db", None)
