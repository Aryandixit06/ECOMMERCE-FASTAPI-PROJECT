from pydantic import BaseModel


class CheckoutRequest(BaseModel):
    coupon_code: str | None = None


class CheckoutResponse(BaseModel):
    order_id: int
    original_amount: float
    discount: float
    final_amount: float
    payment_status: str
    message: str