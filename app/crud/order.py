from sqlalchemy.orm import Session

from app.models.order import Order, OrderItem
from app.models.cart import CartItem
from app.models.product import Product


def create_order(db: Session, user_id: int):
    cart_items = (
        db.query(CartItem)
        .filter(CartItem.user_id == user_id)
        .all()
    )

    if not cart_items:
        return None

    total_price = 0

    order = Order(
        user_id=user_id,
        total_price=0,
        status="Pending",
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart_items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        # Check stock
        if product.stock < item.quantity:
            raise Exception(
                f"{product.name} is out of stock"
            )

        subtotal = product.price * item.quantity
        total_price += subtotal

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price,
        )

        db.add(order_item)

        # Reduce stock
        product.stock -= item.quantity

    order.total_price = total_price

    # Clear user's cart
    db.query(CartItem).filter(
        CartItem.user_id == user_id
    ).delete()

    db.commit()
    db.refresh(order)

    return order


def get_my_orders(db: Session, user_id: int):
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .all()
    )


def get_order_by_id(db: Session, order_id: int):
    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )