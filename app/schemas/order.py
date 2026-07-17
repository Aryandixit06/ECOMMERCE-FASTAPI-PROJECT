from pydantic import BaseModel, ConfigDict
from datetime import datetime


class OrderCreate(BaseModel):
    pass


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str
    created_at: datetime
    order_items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)
    