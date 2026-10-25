import os
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine, Base
from models.product import Product

def seed_products():
    db: Session = SessionLocal()
    
    # Verificamos si ya hay productos para no duplicarlos
    if db.query(Product).count() > 0:
        print("✅ La base de datos ya contiene productos. No se requiere inyección.")
        db.close()
        return

    print("⏳ Inyectando productos de prueba en TiDB...")
    
    # Datos simulando la Fake Store API
    products_data = [
        {
            "title": "Fjallraven - Foldsack No. 1 Backpack",
            "price": 109.95,
            "description": "Your perfect pack for everyday use and walks in the forest. Stash your laptop (up to 15 inches) in the padded sleeve, your everyday",
            "category": "men's clothing",
            "image": "https://fakestoreapi.com/img/81fPKd-2AYL._AC_SL1500_.jpg"
        },
        {
            "title": "Mens Casual Premium Slim Fit T-Shirts ",
            "price": 22.3,
            "description": "Slim-fitting style, contrast raglan long sleeve, three-button henley placket, light weight & soft fabric for breathable and comfortable wearing. And Solid stitched shirts with round neck made for durability and a great fit for casual fashion wear and diehard baseball fans. The Henley style round neckline includes a three-button placket.",
            "category": "men's clothing",
            "image": "https://fakestoreapi.com/img/71-3HjGNDUL._AC_SY879._SX._UX._SY._UY_.jpg"
        },
        {
            "title": "John Hardy Women's Legends Naga Gold & Silver Dragon Station Chain Bracelet",
            "price": 695.00,
            "description": "From our Legends Collection, the Naga was inspired by the mythical water dragon that protects the ocean's pearl. Wear facing inward to be bestowed with love and abundance, or outward for protection.",
            "category": "jewelery",
            "image": "https://fakestoreapi.com/img/71pWzhdJNwL._AC_UL640_QL65_ML3_.jpg"
        },
        {
            "title": "WD 2TB Elements Portable External Hard Drive - USB 3.0 ",
            "price": 64.00,
            "description": "USB 3.0 and USB 2.0 Compatibility Fast data transfers Improve PC Performance High Capacity; Compatibility Formatted NTFS for Windows 10, Windows 8.1, Windows 7; Reformatting may be required for other operating systems",
            "category": "electronics",
            "image": "https://fakestoreapi.com/img/61IBBVJvSDL._AC_SY879_.jpg"
        },
        {
            "title": "BIYLACLESEN Women's 3-in-1 Snowboard Jacket Winter Coats",
            "price": 56.99,
            "description": "Note:The Jackets is US standard size, Please choose size as your usual wear Material: 100% Polyester; Detachable Liner Fabric: Warm Fleece. Detachable Functional Liner: Skin Friendly, Lightweigt and Warm.Stand Collar Liner jacket, keep you warm in cold weather.",
            "category": "women's clothing",
            "image": "https://fakestoreapi.com/img/51Y5NI-I5jL._AC_UX679_.jpg"
        }
    ]

    for item in products_data:
        db_product = Product(**item)
        db.add(db_product)
    
    db.commit()
    print(f"🚀 Se insertaron {len(products_data)} productos exitosamente.")
    db.close()

if __name__ == "__main__":
    seed_products()