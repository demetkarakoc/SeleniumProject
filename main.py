import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.118  Safari/537.3',
    'Accept-Language': 'Turkish;q=1'
}

browser = webdriver.Chrome()
browser.maximize_window()
wait = WebDriverWait(browser, 15)

#Trendyol fiyatları
browser.get("https://www.trendyol.com/sr?q=kalem&qt=kalem&st=kalem&os=1")
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"prc-dsc")))
html_trendyol = browser.page_source
soup_trendyol = BeautifulSoup(html_trendyol,'html.parser')
price_elements_trendyol = soup_trendyol.find_all("div",class_="prc-dsc")
prices_trendyol = [price.text for price in price_elements_trendyol]
print("Trendyol Prices:", prices_trendyol)

#Hepsiburada fiyatları
browser.get("https://www.hepsiburada.com/ara?q=kalem")
wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"turkishLira")))
html_hepsiburada = browser.page_source
soup_hepsiburada = BeautifulSoup(html_hepsiburada,'html.parser')
price_elements_hepsiburada = soup_hepsiburada.find_all("div",class_="turkishLira")
prices_hepsiburada = [price.text for price in price_elements_hepsiburada]
print("Hepsiburada Prices:", prices_hepsiburada)

#DataFrame oluşturma
data = {
    "Website": ["trendyol.com"] * len(prices_trendyol) + ["hepsiburada.com"] * len(prices_hepsiburada),
    "Price": [prices_trendyol, prices_hepsiburada]
}
df = pd.DataFrame(data)

#CSV' ye yazdırma
df.to_csv(r'PriceList.csv', index = False)

browser.quit()
