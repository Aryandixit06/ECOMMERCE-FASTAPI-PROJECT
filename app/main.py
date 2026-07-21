from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine

from app.models import (
    Product,
    User,
    Category,
    CartItem,
    Order,
    OrderItem,
    Wishlist,
    Review,
    Address,
    Coupon,
    Payment,
)

from app.routers import (
    product_router,
    auth_router,
    category_router,
    cart_router,
    order_router,
    wishlist_router,
    review_router,
    address_router,
    coupon_router,
    checkout_router,
    payment_router,
)

app = FastAPI(
    title="E-commerce API",
    version="1.0.0",
)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(product_router)
app.include_router(auth_router)
app.include_router(category_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(wishlist_router)
app.include_router(review_router)
app.include_router(address_router)
app.include_router(coupon_router)
app.include_router(checkout_router)
app.include_router(payment_router)

@app.get("/")
def read_root():
    return {
        "message": "E-commerce API is running!"
    }