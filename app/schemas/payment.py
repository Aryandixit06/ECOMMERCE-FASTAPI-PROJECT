from datetime import datetime
from pydantic import BaseModel


class PaymentCreate(BaseModel):
    order_id: int


class PaymentVerify(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    user_id: int
    razorpay_order_id: str
    razorpay_payment_id: str | None
    amount: float
    currency: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CreatePaymentResponse(BaseModel):
    payment_id: int
    razorpay_order_id: str
    amount: float
    currency: str
    status: str


class VerifyPaymentResponse(BaseModel):
    message: str
    status: str