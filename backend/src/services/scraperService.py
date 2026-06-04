from playwright.async_api import async_playwright as ap
import json

def getCleanUrl(url: str):
    cleanUrl = url.split("/?")[0]
    cleanUrl = cleanUrl.split("/ref")[0]
    return cleanUrl

async def connectToPage(url: str):
    async with ap() as p:
        browser = await p.chromium.launch(
            headless=True
        )
        
        url = getCleanUrl(url)
        print(url)
        page = await browser.new_page()

        await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        #source, product identifier, product url, seller
        #landingImage
        title = await page.title()
        actualName = await page.locator("#productTitle").first.text_content()
        imgSrc = await page.query_selector("#landingImage")
        imgUrl = await imgSrc.get_attribute("src")
        price = await page.locator(".a-price-whole").first.text_content()
        currency = await page.locator(".a-price-symbol").first.text_content()
        mrp = await page.locator(".apex-basisprice-value .a-offscreen").first.text_content()
        discountPercentage = await page.locator(".savingsPercentage").first.text_content()
        reviewCount = await page.locator("#acrCustomerReviewText").first.text_content()
        reviewScore = await page.locator(".mvt-cm-cr-review-stars-mini-popover").first.text_content()
        source = url.split(".")[1]
        productIdentifier = url.split("dp/")[1]

        tableLocators=["#productOverview_feature_div table tr", "#poExpander table tr"]
        count=0
        for locator in tableLocators:
            print(locator)
            rows = page.locator(locator)
            print(rows)
            count = await rows.count()
            print(count)
            if count>0:
                break
        
        miscDetails={}
        for i in range(count):
            row = rows.nth(i)
            key = await row.locator("td:nth-child(1)").inner_text()
            value = await row.locator("td:nth-child(2)").inner_text()
            miscDetails[key.strip()]=value.strip() 

        price = price.replace(",", "").replace(".", "").strip()
        actualName = actualName.strip()
        mrp = mrp[1:].replace(",", "").strip()
        reviewScore = reviewScore.strip()
        reviewScore = reviewScore[:3]
        reviewCount = reviewCount.replace("(", "").replace(")", "").replace(",", "")
        print(miscDetails)
        seller = miscDetails["Brand"]
        discountPercentage = discountPercentage.replace("-", "").replace("%", "")
        # miscDetails = json.dumps(miscDetails)

        print("Connected successfully")
        print("Source:", source)
        print("Page title:", title)
        print("Product name:", actualName)
        print("Currency:", currency)
        print("Price:", price)
        print("MRP:", mrp)
        print("Discount percentage:", discountPercentage)
        print("Review score:", reviewScore)
        print("Review count:", reviewCount)
        print("Product id:", productIdentifier)
        print("Product url:", url)
        print("Seller:", seller)
        print("Miscellaneous details:", miscDetails, "\n", type(miscDetails))

        # await page.pause()
        await browser.close()

        data = {
            "source": source,
            "product_identifier": productIdentifier,
            "product_url": url,
            "image_url": imgUrl,
            "name": actualName,
            "currency": currency,
            "price": float(price),
            "mrp": float(mrp),
            "discount_percentage": float(discountPercentage),
            "review_score": float(reviewScore),
            "review_count": int(reviewCount),
            "seller_company": seller,
            "misc_details": miscDetails
        }

        return data