import sys
import time
from utils.driver_setup import stealth_setup_driver
from utils.save_data import save_to_json
from selenium.common.exceptions import NoSuchWindowException, WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _safe_get(driver_factory, url, headless, max_retries=3, page_load_wait=25, backoff=1.25):
    """
    Navigate to URL with retries. If the window/session is lost, recreate driver.
    Returns (driver, ok_bool).
    """
    driver = driver_factory(headless=headless)
    for attempt in range(max_retries):
        try:
            driver.get(url)
            WebDriverWait(driver, page_load_wait).until(
                lambda d: d.execute_script("return document.readyState") in ("interactive", "complete")
            )
            return driver, True
        except NoSuchWindowException:
            try:
                driver.quit()
            except Exception:
                pass
            time.sleep(backoff * (attempt + 1))
            driver = driver_factory(headless=headless)
        except WebDriverException:
            try:
                driver.quit()
            except Exception:
                pass
            time.sleep(backoff * (attempt + 1))
            driver = driver_factory(headless=headless)
    return driver, False


def _dismiss_cookie_banner(driver):
    # OneTrust accept button is common on Threadless
    try:
        btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        )
        btn.click()
        time.sleep(0.5)
    except Exception:
        pass


def _progressive_scroll(driver, passes=12, pause=0.9):
    for _ in range(passes):
        driver.execute_script("window.scrollBy(0, Math.floor(window.innerHeight*0.9));")
        time.sleep(pause)


def scrape_threadless(pages=1, limit=None, headless=False, start_page=1):
    """
    Scrape Threadless hoodie listings, resilient to UC window loss.
    """
    base_url = (
        "https://www.threadless.com/search/"
        "?sort=popular&departments=mens&style=pullover-hoody&page={page}"
    )

    all_results = []

    for page in range(start_page, start_page + pages):
        if limit and len(all_results) >= limit:
            break

        url = base_url.format(page=page)
        print(f"Scraping Threadless page {page}: {url}")

        # Navigate with retries (recreate driver if needed)
        driver, ok = _safe_get(stealth_setup_driver, url, headless=headless, max_retries=3)
        if not ok:
            print(f"Failed to open page {page}: {url}")
            try:
                driver.quit()
            except Exception:
                pass
            continue

        wait = WebDriverWait(driver, 25)

        # Dismiss cookie banner if present
        _dismiss_cookie_banner(driver)

        # Trigger lazy loading
        _progressive_scroll(driver, passes=12, pause=0.9)

        try:
            # Wait for a broad container selector (class names can vary in headless)
            wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div.results-container-app, div.grid, div#browse-listing, main')
                )
            )
        except TimeoutException as e:
            print(f"Timeout waiting for products on page {page}: {e}")
            try:
                driver.quit()
            except Exception:
                pass
            continue

        # Prefer grid items, fall back to anchors if classnames differ
        product_cards = driver.find_elements(By.CSS_SELECTOR, 'div.grid-item')
        if not product_cards:
            product_cards = driver.find_elements(
                By.CSS_SELECTOR,
                'a.pjax-link.media-image.discover-as-product-linkback-mc, a.sf-shop-design-title.pjax-link'
            )

        count_start = len(all_results)

        for card in product_cards:
            if limit and len(all_results) >= limit:
                break
            try:
                # Product URL
                try:
                    link_elem = card.find_element(
                        By.CSS_SELECTOR, 'a.pjax-link.media-image.discover-as-product-linkback-mc'
                    )
                except Exception:
                    link_elem = card.find_element(By.CSS_SELECTOR, 'a')

                product_url = link_elem.get_attribute("href")

                # Title
                try:
                    title_elem = card.find_element(By.CSS_SELECTOR, 'a.sf-shop-design-title.pjax-link')
                    title = title_elem.text.strip()
                except Exception:
                    title = (link_elem.get_attribute("title") or "").strip()

                # Artist
                try:
                    artist_elem = card.find_element(By.CSS_SELECTOR, 'a.sf-by-line.pjax-link')
                    artist = artist_elem.text.strip()
                except Exception:
                    artist = ""

                # Price
                try:
                    price_elem = card.find_element(By.CSS_SELECTOR, 'span.active_price')
                    price = price_elem.text.strip()
                except Exception:
                    price = ""

                # Image URL
                try:
                    img_elem = card.find_element(By.CSS_SELECTOR, 'img.img-responsive, img')
                    image_url = img_elem.get_attribute("src") or img_elem.get_attribute("data-src")
                except Exception:
                    image_url = ""

                if not product_url or not image_url:
                    continue

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

        print(f"- Collected {len(all_results) - count_start} items from page {page}")

        try:
            driver.quit()
        except Exception:
            pass

    return all_results


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "top10"

    if mode not in ("top10", "all"):
        print("Usage: python scrape_threadless.py [top10|all]")
        return

    # NOT HEADLESS for debugging/visibility
    if mode == "top10":
        data = scrape_threadless(pages=1, limit=10, start_page=1, headless=False)
        save_to_json(data, "top10_threadless.json")
        print(f"Saved {len(data)} hoodies (top 10)")
    else:
        data = scrape_threadless(pages=25, start_page=1, headless=False)  # 48/page, 25 ≈ 1200
        save_to_json(data, "threadless.json")
        print(f"Saved {len(data)} hoodies (all)")


if __name__ == "__main__":
    main()
