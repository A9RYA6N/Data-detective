from sqlalchemy.orm import Session
from src.db.models.productModel import Product

def createProduct(db: Session, data: dict):
    existingProduct = db.query(Product).filter(
        Product.product_identifier == data["product_identifier"]
    ).first()
    if existingProduct:
        return existingProduct

    product = Product(**data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def getAllProducts(db: Session):
    products = db.query(Product).all()
    return products

# def getProductById(db: Session, )