from utils.driver_setup import setup_driver
from utils.save_data import save_to_json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scroll_to_bottom(driver, step=300, pause=0.5):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(pause)  # wait for content to load after scrolling
    current_scroll = driver.execute_script("return window.pageYOffset;")
    while current_scroll > 0:
        new_scroll = max(0, current_scroll - step)
        driver.execute_script(f"window.scrollTo(0, {new_scroll});")
        time.sleep(pause)
        current_scroll = new_scroll


def scrape_society6_hoodies():
    url = "https://society6.com/collections/hoodies"

    driver = setup_driver(headless=False)  # set to True if you don't want the browser to show
    driver.get(url)

    wait = WebDriverWait(driver, 20)

    # Wait for products grid to load - product cards have a 'product-tile' class typically
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol.algolia-products-grid__grid")))

    # Scroll to bottom multiple times to load more products (if any)
    scroll_to_bottom(driver)

    # Now get all product cards
    container = driver.find_element(By.CSS_SELECTOR, "ol.algolia-products-grid__grid")
    product_cards = container.find_elements(By.CSS_SELECTOR, "li.algolia-products-grid__product-item")

    results = []

    for card in product_cards:
        try:
            # Title (usually alt text of image or a span inside card)
            link_container = card.find_element(By.CSS_SELECTOR, "div.product-item__product-gallery")
            link_elem = link_container.find_element(By.TAG_NAME, "a")
            product_url = link_elem.get_attribute("href")
            title = link_elem.get_attribute("aria-label")  # You can get the title from aria-label

            # Artist (inside span with class 'artist-name' or similar)
            artist_elem = card.find_element(By.CSS_SELECTOR, "h3.artist-link")
            artist = artist_elem.find_element(By.TAG_NAME, "a").text.strip()

            # Price (might be inside span with class 'price')
            price_elem = card.find_element(By.CSS_SELECTOR, "span.product-item__product-price-label")
            price = price_elem.text.strip()

            # Image URL
            img_elem = card.find_element(By.CSS_SELECTOR, "img")
            image_url = img_elem.get_attribute("src")

            results.append({
                "title": title,
                "artist": artist,
                "price": price,
                "product_url": product_url,
                "image_url": image_url
            })

        except Exception as e:
            print(f"Error parsing a product card: {e}")
            continue

    driver.quit()
    return results


def main():
    data = scrape_society6_hoodies()
    print(f"Scraped {len(data)} products.")
    save_to_json(data, "society6.json")

if __name__ == "__main__":
    main()
