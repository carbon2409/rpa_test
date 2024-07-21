import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless=new')
chrome_options.add_argument('--disable-gpu')

url = 'https://www.rpachallenge.com/'

with webdriver.Chrome(options=chrome_options) as driver:
    driver.get(url)
    download_link = driver.find_element(By.PARTIAL_LINK_TEXT, 'download').get_attribute('href')
    response = requests.get(download_link)
    with open('challenge.xlsx', 'wb') as file:
        file.write(response.content)

    df = pd.read_excel('challenge.xlsx')
    df.columns = [column.strip() for column in df.columns]
    data = df.to_dict('index')

    driver.find_element(By.XPATH, '/html/body/app-root/div[2]/app-rpa1/div/div[1]/div[6]/button').click()
    for i in range(len(data)):
        person = data[i]
        fields = driver.find_elements(By.TAG_NAME, 'rpa1-field')
        for field in fields:
            field_name = field.find_element(By.TAG_NAME, 'label').text
            field.find_element(By.TAG_NAME, 'input').send_keys(person[field_name])
        driver.find_element(By.XPATH, '/html/body/app-root/div[2]/app-rpa1/div/div[2]/form/input').click()

    driver.save_screenshot('result_1.png')






