from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--enable-automation')

chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--no-sandbox')

url = 'https://www.arealme.com/colors/ru/'

def find_same_color(blocks):
    colors = [block.value_of_css_property('background-color') for block in blocks]
    return Counter(colors).most_common(1)[0][0]


with webdriver.Chrome(options=chrome_options) as driver:
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'start'))).click()
    locator = (By.CLASS_NAME, 'patra-color')
    container = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(locator))
    try:
        while True:
            blocks = container.find_elements(By.TAG_NAME, 'span')
            same_color = find_same_color(blocks[0:3])
            span_number = 0
            for block in blocks:
                span_number += 1
                block_color = block.value_of_css_property('background-color')
                if block_color != same_color:
                    driver.execute_script(f"document.body.querySelector('body > div:nth-child(11) > div:nth-child(1) > \
                    div.patra-color > div > span:nth-child({span_number})').click();")
                    break
    except Exception:
        time.sleep(8)
        driver.save_screenshot('result_2.png')
