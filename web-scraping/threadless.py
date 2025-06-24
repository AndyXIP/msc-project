from utils.driver_setup import setup_driver
from utils.save_data import save_to_json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_threadless_hoodies(pages=25): # 48 hoodies per page, 25 for 1200
    base_url = "https://www.threadless.com/search/?sort=popular&departments=mens&style=pullover-hoody&page={page}"
    driver = setup_driver(headless=False)
    all_results = []

    for page in range(1, pages + 1):
        url = base_url.format(page=page)
        print(f"Scraping Threadless page {page}: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 20)

        # Scroll down multiple times to trigger lazy loading
        for _ in range(6):
            driver.execute_script("window.scrollBy(0, window.innerHeight);")
            time.sleep(1)

        try:
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.results-container-app'))
            )
        except Exception as e:
            print(f"Timeout waiting for products on page {page}: {e}")
            continue

        product_cards = driver.find_elements(By.CSS_SELECTOR, 'div.grid-item')

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

                all_results.append({
                    "title": title,
                    "artist": artist,
                    "price": price,
                    "product_url": product_url,
                    "image_url": image_url
                })
            except Exception as e:
                print(f"Error parsing product card on page {page}: {e}")
                continue

    driver.quit()
    return all_results


def main():
    data = scrape_threadless_hoodies()
    print(f"Scraped total {len(data)} hoodies.")
    save_to_json(data, "threadless.json")

if __name__ == "__main__":
    main()
