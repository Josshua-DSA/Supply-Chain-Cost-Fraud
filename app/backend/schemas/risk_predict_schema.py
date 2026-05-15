"""Schema helpers for late-shipment prediction requests."""


def normalize_records(payload: dict) -> list[dict]:
    if "records" in payload and isinstance(payload["records"], list):
        return payload["records"]
    if "data" in payload and isinstance(payload["data"], list):
        return payload["data"]
    if "data" in payload and isinstance(payload["data"], dict):
        return [payload["data"]]
    return [payload]

"""
schemas/risk.py
---------------
Request and response models for the Late Delivery Risk endpoint.

Input features are derived from the DataCo Supply Chain dataset
plus the engineered features built in Feature_engineering{f&l}.ipynb.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class RiskInput(BaseModel):
    # --- Core order features ---
    Type: Literal["DEBIT", "TRANSFER", "CASH", "PAYMENT"] = Field(
        ..., description="Type of transaction"
    )
    Days_for_shipping_real: int = Field(
        ..., alias="Days for shipping (real)", ge=0,
        description="Actual shipping days"
    )
    Days_for_shipment_scheduled: int = Field(
        ..., alias="Days for shipment (scheduled)", ge=0,
        description="Scheduled delivery days"
    )
    Shipping_Mode: Literal[
        "Standard Class", "First Class", "Second Class", "Same Day"
    ] = Field(..., alias="Shipping Mode")

    # --- Customer / geo ---
    Customer_Segment: Literal["Consumer", "Corporate", "Home Office"] = Field(
        ..., alias="Customer Segment"
    )
    Market: Literal[
        "Africa", "Europe", "LATAM", "Pacific Asia", "USCA"
    ] = Field(...)
    Order_Region: str = Field(..., alias="Order Region")
    Order_Country: str = Field(..., alias="Order Country")
    Customer_Country: str = Field(..., alias="Customer Country")
    Customer_State: str = Field(..., alias="Customer State")
    Order_State: str = Field(..., alias="Order State")
    Customer_City: str = Field(..., alias="Customer City")
    Order_City: str = Field(..., alias="Order City")

    # --- Product / order ---
    Category_Name: str = Field(..., alias="Category Name")
    Department_Name: str = Field(..., alias="Department Name")
    Product_Name: str = Field(..., alias="Product Name")
    Order_Status: str = Field(..., alias="Order Status")

    # --- Financials ---
    Sales: float = Field(..., ge=0)
    Order_Item_Discount: float = Field(..., alias="Order Item Discount", ge=0)
    Order_Item_Discount_Rate: float = Field(..., alias="Order Item Discount Rate", ge=0, le=1)
    Order_Item_Product_Price: float = Field(..., alias="Order Item Product Price", ge=0)
    Order_Item_Profit_Ratio: float = Field(..., alias="Order Item Profit Ratio")
    Order_Item_Quantity: int = Field(..., alias="Order Item Quantity", ge=1)
    Order_Item_Total: float = Field(..., alias="Order Item Total", ge=0)
    Order_Profit_Per_Order: float = Field(..., alias="Order Profit Per Order")
    Benefit_per_order: float = Field(..., alias="Benefit per order")
    Sales_per_customer: float = Field(..., alias="Sales per customer", ge=0)
    Product_Price: float = Field(..., alias="Product Price", ge=0)

    # --- Date features (pre-extracted) ---
    order_year: int = Field(..., ge=2000, le=2100)
    order_month: int = Field(..., ge=1, le=12)
    order_day: int = Field(..., ge=1, le=31)
    order_dayofweek: int = Field(..., ge=0, le=6)
    order_hour: int = Field(..., ge=0, le=23)
    order_is_weekend: int = Field(..., ge=0, le=1)

    # --- Engineered features ---
    actual_delay: Optional[float] = Field(None, description="real - scheduled (can be negative)")
    shipping_speed_ratio: Optional[float] = None
    calculated_item_total: Optional[float] = None
    item_total_gap: Optional[float] = None
    abs_item_total_gap: Optional[float] = None
    has_price_inconsistency: Optional[int] = Field(None, ge=0, le=1)
    country_mismatch: Optional[int] = Field(None, ge=0, le=1)
    state_mismatch: Optional[int] = Field(None, ge=0, le=1)
    city_mismatch: Optional[int] = Field(None, ge=0, le=1)

    class Config:
        populate_by_name = True


class RiskResponse(BaseModel):
    prediction: int = Field(..., description="0 = on time, 1 = late delivery risk")
    probability_late: float = Field(..., ge=0.0, le=1.0, description="Probability of late delivery")
    probability_on_time: float = Field(..., ge=0.0, le=1.0)
    label: str = Field(..., description="Human-readable label")
    model_version: str = "0.1.0"


class BatchRiskInput(BaseModel):
    orders: list[RiskInput]


class BatchRiskResponse(BaseModel):
    results: list[RiskResponse]
    total: int
    late_count: int
    on_time_count: int