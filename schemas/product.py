from pydantic import BaseModel

class ProductBase(BaseModel):
    title: str
    price: float
    description: str
    category: str
    image: str

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True
