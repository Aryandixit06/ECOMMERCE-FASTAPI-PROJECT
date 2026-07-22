from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    is_active: bool = True

    image_url: str | None = None
    brand: str | None = None
    rating: float = 0.0
    discount_percentage: int = 0

    category_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    is_active: bool | None = None

    image_url: str | None = None
    brand: str | None = None
    rating: float | None = None
    discount_percentage: int | None = None

    category_id: int | None = None


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)