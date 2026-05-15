"""
services/order_service.py
--------------------------
CRUD operations untuk collection `orders` dan `order_items`.
"""

import logging
from typing import Optional, List
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

from backend.schemas.db_models import OrderDocument, OrderItemDocument, PredictionLogDocument

logger = logging.getLogger(__name__)


# ─── Orders ──────────────────────────────────────────────────────────────────

async def get_order_by_id(db: AsyncIOMotorDatabase, order_id: int) -> Optional[dict]:
    return await db.orders.find_one({"order_id": order_id}, {"_id": 0})


async def get_orders(
    db: AsyncIOMotorDatabase,
    skip: int = 0,
    limit: int = 50,
    market: Optional[str] = None,
    late_delivery_risk: Optional[int] = None,
    shipping_mode: Optional[str] = None,
) -> List[dict]:
    query = {}
    if market:
        query["market"] = market
    if late_delivery_risk is not None:
        query["late_delivery_risk"] = late_delivery_risk
    if shipping_mode:
        query["shipping_mode"] = shipping_mode

    cursor = db.orders.find(query, {"_id": 0}).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


async def insert_order(db: AsyncIOMotorDatabase, order: OrderDocument) -> str:
    result = await db.orders.insert_one(order.dict())
    return str(result.inserted_id)


async def insert_orders_bulk(db: AsyncIOMotorDatabase, orders: List[OrderDocument]) -> int:
    docs = [o.dict() for o in orders]
    result = await db.orders.insert_many(docs, ordered=False)
    return len(result.inserted_ids)


async def count_orders(
    db: AsyncIOMotorDatabase,
    market: Optional[str] = None,
    late_delivery_risk: Optional[int] = None,
) -> int:
    query = {}
    if market:
        query["market"] = market
    if late_delivery_risk is not None:
        query["late_delivery_risk"] = late_delivery_risk
    return await db.orders.count_documents(query)


# ─── Order Items ──────────────────────────────────────────────────────────────

async def get_items_by_order(db: AsyncIOMotorDatabase, order_id: int) -> List[dict]:
    cursor = db.order_items.find({"order_id": order_id}, {"_id": 0})
    return await cursor.to_list(length=100)


async def insert_order_items_bulk(
    db: AsyncIOMotorDatabase, items: List[OrderItemDocument]
) -> int:
    docs = [i.dict() for i in items]
    result = await db.order_items.insert_many(docs, ordered=False)
    return len(result.inserted_ids)


# ─── Prediction Log ───────────────────────────────────────────────────────────

async def log_prediction(
    db: AsyncIOMotorDatabase,
    prediction_doc: PredictionLogDocument,
) -> str:
    result = await db.predictions.insert_one(prediction_doc.dict())
    return str(result.inserted_id)


async def get_prediction_logs(
    db: AsyncIOMotorDatabase,
    skip: int = 0,
    limit: int = 50,
    prediction: Optional[int] = None,
) -> List[dict]:
    query = {}
    if prediction is not None:
        query["prediction"] = prediction
    cursor = db.predictions.find(query, {"_id": 0}).sort("created_at", -1).skip(skip).limit(limit)
    return await cursor.to_list(length=limit)


# ─── Analytics queries ────────────────────────────────────────────────────────

async def get_risk_summary(db: AsyncIOMotorDatabase) -> dict:
    """Aggregate: jumlah late vs on-time per market."""
    pipeline = [
        {"$group": {
            "_id": {
                "market": "$market",
                "late_delivery_risk": "$late_delivery_risk"
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.market": 1}}
    ]
    cursor = db.orders.aggregate(pipeline)
    results = await cursor.to_list(length=None)
    return {"summary": results}


async def get_sales_by_category(db: AsyncIOMotorDatabase) -> dict:
    """Aggregate: total sales per category."""
    pipeline = [
        {"$group": {
            "_id": "$category_name",
            "total_sales": {"$sum": "$sales_per_customer"},
            "total_profit": {"$sum": "$order_profit_per_order"},
            "order_count": {"$sum": 1}
        }},
        {"$sort": {"total_sales": -1}},
        {"$limit": 20}
    ]
    cursor = db.orders.aggregate(pipeline)
    results = await cursor.to_list(length=None)
    return {"categories": results}