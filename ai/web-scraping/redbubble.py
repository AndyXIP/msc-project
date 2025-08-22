import sys
import time
from utils.driver_setup import setup_driver
from utils.save_data import save_to_json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scrape_redbubble(pages=1, limit=None, headless=False, start_page=1):  # <-- added start_page
    """
    Scrape Redbubble hoodie listings.

    Args:
        pages (int): number of pages to scrape starting from `start_page`.
        limit (int|None): stop early after collecting this many items.
        headless (bool): run browser headless.
        start_page (int): FIRST page number to scrape (default 1).
    """
    base_url = (
        "https://www.redbubble.com/shop"
        "?country=GB&iaCode=u-sweatshirts&locale=en&page={page}&sortOrder=trending"
    )
    driver = setup_driver(headless=headless)
    all_results = []

    # iterate from start_page up to start_page + pages - 1
    for page in range(start_page, start_page + pages):
        url = base_url.format(page=page)
        print(f"Scraping page {page}: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 20)

        # Scroll down to trigger lazy loading
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(1)

        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.styles_box__54ba70e3.SearchResultsGrid_grid__z2G0D')
                )
            )
        except Exception as e:
            print(f"Timeout waiting for products on page {page}: {e}")
            continue

        product_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="search-result-card"]')

        for card in product_cards:
            try:
                link_elem = card.find_element(By.CSS_SELECTOR, 'a.styles_link__51d7d395')
                product_url = link_elem.get_attribute("href")

                title_elem = card.find_element(By.CSS_SELECTOR, 'span.styles_text__5c7a80ef')
                title = title_elem.text.strip()

                artist_elem = card.find_element(By.XPATH, './/span[contains(text(), "By ")]')
                artist = artist_elem.text.replace("By ", "").strip()

                price_elem = card.find_element(By.CSS_SELECTOR, 'span[data-testid="line-item-price-price"]')
                price = price_elem.text.strip()

                img_elem = card.find_element(By.CSS_SELECTOR, 'img.ProductCard_productCardImage____xct')
                image_url = img_elem.get_attribute("src")

                all_results.append({
                    "title": title,
                    "artist": artist,
                    "price": price,
                    "product_url": product_url,
                    "image_url": image_url
                })

                # Stop early if limit reached
                if limit and len(all_results) >= limit:
                    driver.quit()
                    return all_results

            except Exception as e:
                print(f"Error parsing product card on page {page}: {e}")
                continue

    driver.quit()
    return all_results


def main():
    # Get mode from CLI (default to "top10")
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"

    if mode not in ("top10", "all"):
        print("Usage: python scrape_redbubble.py [top10|all]")
        return

    if mode == "top10":
        hoodies = scrape_redbubble(pages=1, limit=10, start_page=1, headless=True)  # now explicit
        save_to_json(hoodies, "top10_redbubble.json")
        print(f"Saved {len(hoodies)} hoodies (top 10)")
    else:
        hoodies = scrape_redbubble(pages=10, start_page=1, headless=True)
        save_to_json(hoodies, "redbubble.json")
        print(f"Saved {len(hoodies)} hoodies (all)")


if __name__ == "__main__":
    main()
