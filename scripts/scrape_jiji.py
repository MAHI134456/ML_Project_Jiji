import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

base_url = "https://jiji.com.et/mobile-phones"
num_pages = 24

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.7680.71 Safari/537.36')

driver = webdriver.Chrome(options=options)

data = []

try:
    for page in range(1, num_pages + 1):
        page_url = f"{base_url}?page={page}"
        print(f"Loading page {page_url}")
        driver.get(page_url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.qa-advert-list-item"))
            )
        except TimeoutException:
            print(f"Timeout waiting for ads on page {page}")
            continue

        items = driver.find_elements(By.CSS_SELECTOR, "a.qa-advert-list-item")
        print(f"Found {len(items)} listing items on page {page}")

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, ".qa-advert-list-item-title").text.strip()
            except (NoSuchElementException, Exception):
                title = ""
            try:
                price_text = item.find_element(By.CSS_SELECTOR, ".qa-advert-price").text.strip()
            except (NoSuchElementException, Exception):
                price_text = ""
            try:
                location = item.find_element(By.CSS_SELECTOR, ".b-list-advert__region").text.strip()
            except (NoSuchElementException, Exception):
                location = ""

            if not title and not price_text:
                continue

            # Normalize price
            price_clean = re.sub(r"[^\d]", "", price_text)
            if price_clean:
                try:
                    price_val = int(price_clean)
                except ValueError:
                    price_val = None
            else:
                price_val = None

            # Add brand/storage heuristics
            brand_match = re.search(r"(Samsung|iPhone|Tecno|Infinix|Huawei|Xiaomi|itel|Nokia)", title, re.I)
            brand = brand_match.group(0) if brand_match else "Other"
            storage_match = re.search(r"(\d+\s?GB|\d+GB)", title, re.I)
            storage = storage_match.group(0).replace(' ', '') if storage_match else ""
            condition = "Used" if re.search(r"used|second hand|pre-owned", title + ' ' + item.text, re.I) else "New"

            data.append({
                "Title": title,
                "Brand": brand,
                "Storage": storage,
                "Condition": condition,
                "Location": location,
                "Price": price_val,
                "RawPrice": price_text,
                "Page": page,
            })

        time.sleep(1)

finally:
    driver.quit()

if data:
    df = pd.DataFrame(data)
    df.to_csv("data/raw/jiji_smartphones_raw.csv", index=False)
    print(f"Scraping finished! Saved {len(df)} rows to jiji_smartphones_raw.csv")
else:
    print("No data scraped.")