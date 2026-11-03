from typing import Optional
from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    price: float
    description: Optional[str] = ""
    category: str
    image: Optional[str] = ""


class ProductCreate(ProductBase):
    """Payload para crear un producto nuevo (POST /products/ — solo admin1)."""
    pass


class ProductUpdate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
