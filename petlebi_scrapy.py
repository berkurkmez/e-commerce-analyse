from bs4 import BeautifulSoup as bts
import requests
import time,os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
##import warnings warnings.filterwarnings (action='ignore')
from selenium.webdriver.common.by import By
import json
import pandas as pd

#chromedriver lokasyonu girilecek
chromedriver = "chromedriver"
os.environ["webdriver_chrome.driver"] = chromedriver

search = 'https://www.petlebi.com/kopek-kapisi'

product_URL = []
product_name = []
product_barcode = []
product_price = []
#product_stock = []
#product_images = []
description = []
#sku = []
category = []
#product_ID = [] MySQL'e atarken kendisi oluşturuyor
brand = []

driver = webdriver.Chrome(chromedriver)
driver.get(search)

soup = bts(driver.page_source, "html.parser")

for title in soup.find("div", {"id": "products"}).findAll("h3", {"class":"commerce-title mt-2 mb-0"}):
    title = title.text.strip()
    link = driver.find_element(By.PARTIAL_LINK_TEXT, title)
    link.click()

    soup = bts(driver.page_source, "html.parser")
    time.sleep(3)
    #link'in listeye eklendiği yer
    link_element = driver.current_url
    product_URL.append(link_element)
    
    #ürün isminin listeye eklendiği yer
    product_title = soup.find("h1", {"class":"product-h1"})
    if product_title:
        product_name.append(product_title.text.strip())
    else:
        product_name.append(None)

    #ürün barkod listeye eklendiği yer
    product_barcode_number = soup.find("div", {"id": "hakkinda"}).findAll("div", {"class":"col-10 pd-d-v"})[2].text
    if product_barcode_number:
        product_barcode.append(product_barcode_number)
    else:
        product_barcode.append(None)

    #fiyat'ın listeye eklendiği yer
    new_price = soup.find("p", {"class":"new-price"}).text.strip().split()[0]
    if new_price:
        product_price.append(new_price.strip())
    else:
        product_price.append(None)
    
    #stok bilgisi bulunamamıştır.
    #!!!!!!!!!görsel eklenecektir.
    

    #ürün açıklamasının listeye eklendiği yer
    #database'de sorun çıktığı için 0-20 karakterde sınırlandırılmıştır.
    product_description = soup.find("span", {"id": "productDescription"}).text.strip()[0:20]
    if product_description:
        description.append(product_description)
    else:
        description.append(None)
    
    #sku eklenecektir.
    
    #ürünün kategorisinin eklenediği yer
    product_category = soup.find("ol", {"class": "breadcrumb"}).text.strip()
    product_category = '-'.join(product_category.strip().split('\n'))
    if product_category:
        category.append(product_category)
    else:
        category.append(None)
    
    #ürünün markasının eklenediği yer
    product_brand = soup.find("div", {"id": "hakkinda"}).findAll("div", {"class":"col-10 pd-d-v"})[0].text
    if product_brand:
        brand.append(product_brand)
    else:
        brand.append(None)

    driver.back()

    if driver.current_url == link_element:
        driver.back()

    soup = bts(driver.page_source, "html.parser")



driver.close()
driver.quit()

data = {
    "product_URL": product_URL,
    "product_name": product_name,
    "barcode": product_barcode,
    "price": product_price,
    "description": description,
    "category": category,
    "brand": brand

}

df = pd.DataFrame(data)

json_data = df.to_json(orient="records")

with open("petlebi_products.json", "w") as file:
    file.write(json_data)

