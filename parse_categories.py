from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://kaspi.kz/shop/c/categories/")
time.sleep(5)  # ждем, пока прогрузится JS

# Находим все основные категории
categories = driver.find_elements(By.CSS_SELECTOR, "ul.categories__list > li > span.categories__title")

for cat in categories:
    print("Категория:", cat.text)
    cat.click()
    time.sleep(2)

    # Находим подкатегории внутри этой категории
    subcategories = driver.find_elements(By.CSS_SELECTOR, "ul.subcategories__list > li > span.subcategories__title")
    for sub in subcategories:
        print("  Подкатегория:", sub.text)
        sub.click()
        time.sleep(2)

        # Находим подподкатегории (если есть)
        sub_subcategories = driver.find_elements(By.CSS_SELECTOR, "ul.subsubcategories__list > li > span.subsubcategories__title")
        for subsub in sub_subcategories:
            print("    Подподкатегория:", subsub.text)

driver.quit()
