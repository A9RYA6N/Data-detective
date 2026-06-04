from sqlalchemy.orm import Session
from src.db.models.productModel import Product

def createProduct(db: Session, data: dict):
    existingProduct = db.query(Product).filter(
        Product.product_identifier == data["product_identifier"]
    ).first()
    if existingProduct:
        return {
            "product": existingProduct,
            "existed": True
        }

    product = Product(**data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return {
        "product": product, 
        "existed": False
    }

def getAllProducts(db: Session):
    products = db.query(Product).all()
    return products

def getAllProductsUrlAndId(db: Session):
    prodIdentifiers = db.query(Product.id, Product.product_url).all()
    result = [{"id":r[0], "url":r[1]} for r in prodIdentifiers]
    print(result)
    print(prodIdentifiers)
    return result

# def getProductById(db: Session, )