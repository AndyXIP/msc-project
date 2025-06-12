from driver_setup import setup_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def scrape_redbubble_hoodies():
    url = "https://www.threadless.com/search/?sort=popular&departments=mens&style=pullover-hoody"

    driver = setup_driver(headless=False)
    driver.get(url)

    wait = WebDriverWait(driver, 20)  # wait longer because page loads JS

    # Scroll down to trigger lazy loading (scroll 3 times with pause)
    for _ in range(6):
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(1)

    # Wait for the container holding products
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results-container-app'))
    )

    product_cards = driver.find_elements(By.CSS_SELECTOR, 'div.grid-item')

    results = []

    for card in product_cards:
        try:
            link_elem = card.find_element(By.CSS_SELECTOR, 'a.pjax-link.media-image.discover-as-product-linkback-mc')
            product_url = link_elem.get_attribute("href")

            title_elem = card.find_element(By.CSS_SELECTOR, 'a.sf-shop-design-title.pjax-link')
            title = title_elem.text.strip()

            artist_elem = card.find_element(By.CSS_SELECTOR, 'a.sf-by-line.pjax-link')
            artist = artist_elem.text.strip()

            price_elem = card.find_element(By.CSS_SELECTOR, 'span.active_price')
            price = price_elem.text.strip()

            img_elem = card.find_element(By.CSS_SELECTOR, 'img.img-responsive')
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

def save_to_json(data, filename="./hoodie data/threadless_hoodies.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    hoodies = scrape_redbubble_hoodies()
    print(f"Found {len(hoodies)} hoodies:")
    for h in hoodies:
        print(h["title"], "-", h["price"])
    save_to_json(hoodies)

if __name__ == "__main__":
    main()
