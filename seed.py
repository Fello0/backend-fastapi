from config.database import SessionLocal
from models.product import Product

def seed_data():
    db = SessionLocal()
    
    print("Eliminando productos antiguos...")
    db.query(Product).delete()
    db.commit()
    
    print("Inyectando catálogo propio...")
    custom_products = [
        {
            "title": "Laptop Developer Pro 15\"",
            "price": 1299.99,
            "description": "Equipo de alto rendimiento ideal para programar, compilar código y correr contenedores con 32GB de RAM.",
            "category": "electronics",
            "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=500&q=80"
        },
        {
            "title": "Monitor UltraWide 34\"",
            "price": 450.00,
            "description": "Monitor curvo perfecto para tener múltiples ventanas de Visual Studio Code abiertas al mismo tiempo.",
            "category": "electronics",
            "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?auto=format&fit=crop&w=500&q=80"
        },
        {
            "title": "Mochila Urbana Resistente al Agua",
            "price": 45.50,
            "description": "Mochila con compartimento acolchado para laptop, ideal para estudiantes y profesionales.",
            "category": "men's clothing",
            "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=500&q=80"
        },
        {
            "title": "Reloj Inteligente Minimalista",
            "price": 199.99,
            "description": "Reloj de diseño elegante con notificaciones, monitoreo de salud y batería de larga duración.",
            "category": "jewelery",
            "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80"
        },
        {
            "title": "Sudadera Básica de Algodón",
            "price": 35.00,
            "description": "Sudadera muy cómoda para esos días largos frente a la computadora.",
            "category": "women's clothing",
            "image": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=500&q=80"
        }
    ]

    for item in custom_products:
        prod = Product(**item)
        db.add(prod)
    
    db.commit()
    db.close()
    print("¡Catálogo inyectado correctamente en TiDB Cloud!")

if __name__ == "__main__":
    seed_data()