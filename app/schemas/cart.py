from pydantic import BaseModel, ConfigDict


class CartBase(BaseModel):
    product_id: int
    quantity: int


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    quantity: int


class CartResponse(CartBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)