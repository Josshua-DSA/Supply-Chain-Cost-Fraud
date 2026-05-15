"""
schemas/db_models.py
---------------------
Struktur dokumen MongoDB untuk setiap collection.
Menggunakan Pydantic v2 untuk validasi saat insert/read.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId


# ─── Helper ──────────────────────────────────────────────────────────────────

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


# ─── Collection: orders ───────────────────────────────────────────────────────

class OrderDocument(BaseModel):
    """
    Satu dokumen di collection `orders`.
    Mewakili satu baris dari DataCoSupplyChainDataset.
    """
    order_id: int
    order_date: Optional[datetime] = None
    shipping_date: Optional[datetime] = None

    # Customer
    customer_id: int
    customer_segment: Optional[str] = None
    customer_city: Optional[str] = None
    customer_state: Optional[str] = None
    customer_country: Optional[str] = None

    # Shipping
    shipping_mode: Optional[str] = None
    days_for_shipping_real: Optional[int] = None
    days_for_shipment_scheduled: Optional[int] = None
    delivery_status: Optional[str] = None
    late_delivery_risk: Optional[int] = None  # 0 or 1

    # Geography
    market: Optional[str] = None
    order_region: Optional[str] = None
    order_country: Optional[str] = None
    order_city: Optional[str] = None
    order_state: Optional[str] = None

    # Financials
    sales_per_customer: Optional[float] = None
    benefit_per_order: Optional[float] = None
    order_profit_per_order: Optional[float] = None
    order_status: Optional[str] = None
    type: Optional[str] = None  # transaction type

    # Product
    product_card_id: Optional[int] = None
    product_name: Optional[str] = None
    product_price: Optional[float] = None
    product_status: Optional[int] = None
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None

    # Store geo
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    # Engineered features (opsional, bisa di-populate setelah feature engineering)
    actual_delay: Optional[float] = None
    shipping_speed_ratio: Optional[float] = None
    has_price_inconsistency: Optional[int] = None
    country_mismatch: Optional[int] = None
    state_mismatch: Optional[int] = None
    city_mismatch: Optional[int] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


# ─── Collection: order_items ──────────────────────────────────────────────────

class OrderItemDocument(BaseModel):
    """
    Satu dokumen di collection `order_items`.
    Relasi ke orders via order_id.
    """
    order_item_id: int
    order_id: int
    product_card_id: Optional[int] = None
    order_item_cardprod_id: Optional[int] = None
    order_item_quantity: Optional[int] = None
    order_item_product_price: Optional[float] = None
    order_item_discount: Optional[float] = None
    order_item_discount_rate: Optional[float] = None
    order_item_profit_ratio: Optional[float] = None
    sales: Optional[float] = None
    order_item_total: Optional[float] = None

    # Engineered
    calculated_item_total: Optional[float] = None
    item_total_gap: Optional[float] = None
    abs_item_total_gap: Optional[float] = None

    class Config:
        populate_by_name = True


# ─── Collection: predictions ──────────────────────────────────────────────────

class PredictionLogDocument(BaseModel):
    """
    Log setiap kali endpoint /risk/predict dipanggil.
    Berguna untuk monitoring model drift.
    """
    order_id: Optional[int] = None           # referensi ke orders (jika ada)
    prediction: int                           # 0 or 1
    probability_late: float
    probability_on_time: float
    label: str
    model_version: str
    input_snapshot: dict                      # raw input yang dikirim
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True


# ─── Collection: forecast_logs ────────────────────────────────────────────────

class ForecastLogDocument(BaseModel):
    category_name: str
    market: str
    periods: int
    forecast_result: List[dict]
    model_version: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True