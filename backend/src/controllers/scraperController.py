from sqlalchemy.orm import Session

from src.schema.request import Url
from src.services.scraperService import connectToPage
from src.db.repo.productRepo import createProduct, getAllProducts

async def scrapeController(url: Url, db: Session):
    data = await connectToPage(url.url)
    print(data)
    for key, value in data.items():
        print(key, value, type(value))
    
    product = createProduct(db, data)
    print(product.id)

    return{
        "success": True,
        "message": "Scraped data"
    }

async def getAllDataController(db: Session):
    data = getAllProducts(db)
    return{
        "success":True,
        "message":"Data fetched successfully",
        "data": data
    }