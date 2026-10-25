from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.product import Product
from schemas.product import ProductUpdate

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

    def update_product(self, product_id: int, payload: ProductUpdate):
        """Actualiza un producto existente en TiDB. Solo alcanzable por admin1."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no disponible")

        title = (payload.title or "").strip()
        if not title:
            raise HTTPException(status_code=400, detail="El título del producto es obligatorio.")

        if payload.price is None or payload.price < 0:
            raise HTTPException(
                status_code=400,
                detail="El precio debe ser un número mayor o igual a 0.",
            )

        product.title = title
        product.price = payload.price
        product.description = payload.description
        product.category = payload.category
        product.image = payload.image

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int):
        """Elimina un producto de forma real en TiDB. Solo alcanzable por admin1."""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Producto no disponible")

        title = product.title
        self.db.delete(product)
        self.db.commit()

        return {
            "message": f"Producto '{title}' eliminado correctamente",
            "id": product_id,
        }
