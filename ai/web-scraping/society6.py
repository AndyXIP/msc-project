import sys
import time
from utils.driver_setup import setup_driver
from utils.save_data import save_to_json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def scroll_to_bottom(driver, step=300, pause=0.75):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)  # wait for content to load after scrolling
    current_scroll = driver.execute_script("return window.pageYOffset;")
    while current_scroll > 0:
        new_scroll = max(0, current_scroll - step)
        driver.execute_script(f"window.scrollTo(0, {new_scroll});")
        time.sleep(pause)
        current_scroll = new_scroll


def scrape_society6(pages=1, limit=None, headless=False): # 30 per page, 21 pages max
    base_url = "https://society6.com/collections/hoodies?page={page}"
    driver = setup_driver(headless=headless)
    wait = WebDriverWait(driver, 20)
    all_results = []

    for page in range(1, pages + 1):
        url = base_url.format(page=page)
        print(f"Scraping Society6 page {page}: {url}")
        driver.get(url)

        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ol.algolia-products-grid__grid"))
        )

        scroll_to_bottom(driver)

        container = driver.find_element(By.CSS_SELECTOR, "ol.algolia-products-grid__grid")
        product_cards = container.find_elements(By.CSS_SELECTOR, "li.algolia-products-grid__product-item")

        for card in product_cards:
            try:
                link_container = card.find_element(By.CSS_SELECTOR, "div.product-item__product-gallery")
                link_elem = link_container.find_element(By.TAG_NAME, "a")
                product_url = link_elem.get_attribute("href")
                title = link_elem.get_attribute("aria-label")

                artist_elem = card.find_element(By.CSS_SELECTOR, "div.artist-link")
                artist = artist_elem.find_element(By.TAG_NAME, "a").text.strip()

                price_elem = card.find_element(By.CSS_SELECTOR, "span.product-item__product-price-label")
                price = price_elem.text.strip()

                img_elem = card.find_element(By.CSS_SELECTOR, "img")
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
                print(f"Error parsing a product card: {e}")
                continue

    driver.quit()
    return all_results


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"

    if mode not in ("top10", "all"):
        print("Usage: python scrape_society6.py [top10|all]")
        return

    if mode == "top10":
        data = scrape_society6(pages=1, limit=10)
        save_to_json(data, "top10_society6.json")
        print(f"Saved {len(data)} hoodies (top 10)")
    else:
        data = scrape_society6(pages=21)  # 21 pages max
        save_to_json(data, "society6.json")
        print(f"Saved {len(data)} hoodies (all)")


if __name__ == "__main__":
    main()
