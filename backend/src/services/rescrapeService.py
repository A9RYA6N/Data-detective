from playwright.async_api import async_playwright as ap
from src.db.repo.productRepo import getAllProductsUrlAndId
from src.config.db import SessionLocal
from src.db.repo.snapshotRepo import createSnapshot
import asyncio

async def rescrapeData():
    db=SessionLocal()

    data = getAllProductsUrlAndId(db=db)
    result=[]
    async with ap() as p:
        browser = await p.chromium.launch(
            headless=True
        )
        i=0
        page = await browser.new_page()
        await page.route("**/*", lambda route:
                    route.abort() if route.request.resource_type in ["image", "media", "font", "stylesheet"]
                    else route.continue_())
        
        for product in data:
            i+=1
            print("Rescraping all data, Count:", i)
            
            await page.goto(
                url=product["url"],
                wait_until="domcontentloaded",
                timeout=60000
            )
            print("Current url:", product["url"])
            price = await page.locator(".a-price-whole").first.text_content()
            mrp = await page.locator(".apex-basisprice-value .a-offscreen").first.text_content()
            discountPercentage = await page.locator(".savingsPercentage").first.text_content()
            reviewCount = await page.locator("#acrCustomerReviewText").first.text_content()
            reviewScore = await page.locator(".mvt-cm-cr-review-stars-mini-popover").first.text_content()

            price = price.replace(",", "").replace(".", "").strip()
            mrp = mrp[1:].replace(",", "").strip()
            reviewScore = reviewScore.strip()
            reviewScore = reviewScore[:3]
            reviewCount = reviewCount.replace("(", "").replace(")", "").replace(",", "")
            discountPercentage = discountPercentage.replace("-", "").replace("%", "")

            print("Price", price)
            print("Mrp", mrp)
            print("Discount percentage", discountPercentage)
            print("Review count", reviewCount)
            print("Review score", reviewScore)
            scrapedData = {
                "product_id": product["id"],
                "price": price,
                "mrp": mrp,
                "discount_percentage": discountPercentage,
                "review_count": reviewCount,
                "review_score": reviewScore
            }

            await asyncio.to_thread(createSnapshot, db, scrapedData)
            print(f"Snapshot created for product id: {product['id']}")

            result.append(scrapedData)
            
        await browser.close()
        print("Rescraping finished without any issues")
    print(result)
    return result