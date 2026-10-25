from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.product import Product

class ProductController:
    def __init__(self, db: Session):
        self.db = db

    def get_all_products(self):
        return self.db.query(Product).all()

    def get_all_categories(self):
        # Obtiene solo las categorías únicas de la tabla products para los filtros
        categories = self.db.query(Product.category).distinct().all()
        return [cat[0] for cat in categories]

    def get_products_by_category(self, category: str):
        return self.db.query(Product).filter(Product.category == category).all()

    def get_product_by_id(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            # Manejo de error de consulta exigido en US05
            raise HTTPException(status_code=404, detail="Producto no disponible")
        return product