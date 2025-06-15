from utils.driver_setup import setup_driver
from utils.save_data import save_to_json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_redbubble_hoodies():
    url = "https://www.redbubble.com/shop/hoodies"

    driver = setup_driver(headless=False)
    driver.get(url)

    wait = WebDriverWait(driver, 20)  # wait longer because page loads JS

    # Scroll down to trigger lazy loading (scroll 3 times with pause)
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1)

    # Wait for the container holding products
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.styles_box__54ba70e3.SearchResultsGrid_grid__z2G0D'))
    )

    product_cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="search-result-card"]')

    results = []

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

            results.append({
                "title": title,
                "artist": artist,
                "price": price,
                "product_url": product_url,
                "image_url": image_url
            })
        except Exception as e:
            print(f"Error parsing product card: {e}")
            continue

    driver.quit()
    return results


def main():
    hoodies = scrape_redbubble_hoodies()
    print(f"Found {len(hoodies)} hoodies:")
    for h in hoodies:
        print(h["title"], "-", h["price"])
    save_to_json(hoodies, "redbubble.json")

if __name__ == "__main__":
    main()
