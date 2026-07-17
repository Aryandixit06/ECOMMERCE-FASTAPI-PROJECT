from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime


class AddressBase(BaseModel):
    full_name: str = Field(..., min_length=3, max_length=100)
    phone: str = Field(..., min_length=10, max_length=15)
    address_line: str = Field(..., min_length=5, max_length=255)
    city: str
    state: str
    country: str = "India"
    postal_code: str
    address_type: str = "Home"


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    address_line: str | None = None
    city: str | None = None
    state: str | None = None
    country: str | None = None
    postal_code: str | None = None
    address_type: str | None = None
    is_default: bool | None = None


class AddressResponse(AddressBase):
    id: int
    user_id: int
    is_default: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)