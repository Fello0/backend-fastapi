from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from config.database import get_db
from schemas.product import ProductResponse
from controllers.product_controller import ProductController

router = APIRouter(prefix="/products", tags=["Productos"])

@router.get("/", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    controller = ProductController(db)
    return controller.get_all_products()

@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    controller = ProductController(db)
    return controller.get_all_categories()

@router.get("/category/{category}", response_model=List[ProductResponse])
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    controller = ProductController(db)
    return controller.get_products_by_category(category)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    controller = ProductController(db)
    return controller.get_product_by_id(product_id)