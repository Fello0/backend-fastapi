from sqlalchemy import Column, Integer, String, Float, Text
from config.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String(100), index=True, nullable=False)
    image = Column(String(255), nullable=True)