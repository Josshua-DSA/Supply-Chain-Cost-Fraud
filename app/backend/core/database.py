"""
core/database.py
-----------------
MongoDB connection manager menggunakan Motor (async driver).

Collections:
  - orders          → data order lengkap dari supply chain
  - order_items     → detail item per order
  - predictions     → log hasil prediksi risk model
  - forecast_logs   → log hasil demand forecast
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from backend.core.config import settings

logger = logging.getLogger(__name__)


class MongoDB:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect(self):
        logger.info(f"Connecting to MongoDB: {settings.MONGODB_URI}")
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB_NAME]
        # Ping untuk pastikan koneksi berhasil
        await self.client.admin.command("ping")
        logger.info(f"Connected to MongoDB database: {settings.MONGODB_DB_NAME}")
        await self._create_indexes()

    async def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed.")

    async def _create_indexes(self):
        """Buat indexes penting agar query cepat."""
        # orders
        await self.db.orders.create_index("order_id", unique=True)
        await self.db.orders.create_index("order_date")
        await self.db.orders.create_index("customer_id")
        await self.db.orders.create_index("late_delivery_risk")

        # order_items
        await self.db.order_items.create_index("order_id")
        await self.db.order_items.create_index("order_item_id", unique=True)

        # predictions log
        await self.db.predictions.create_index("order_id")
        await self.db.predictions.create_index("created_at")
        await self.db.predictions.create_index("prediction")

        # forecast log
        await self.db.forecast_logs.create_index("created_at")
        await self.db.forecast_logs.create_index("category_name")

        logger.info("MongoDB indexes created.")

    def get_db(self) -> AsyncIOMotorDatabase:
        return self.db


mongodb = MongoDB()


async def get_db() -> AsyncIOMotorDatabase:
    """FastAPI dependency — inject ke router."""
    return mongodb.get_db()