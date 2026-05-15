from playwright.async_api import async_playwright as ap

async def connectToPage(url: str):
    async with ap() as p:
        browser = await p.chromium.launch(
            headless=False
        )

        page = await browser.new_page()

        await page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        title = await page.title()
        actualName = await page.locator("#productTitle").first.text_content()
        price = await page.locator(".a-price-whole").first.text_content()
        price = price.replace(",", "").replace(".", "").strip()
        actualName = actualName.strip()

        print("Connected successfully")
        print("Page title:", title)
        print("Product name:", actualName)
        print("Price", price)

        await browser.close()

        return{
            "success": True,
            "title": title
        }