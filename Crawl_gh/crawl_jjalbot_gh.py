# %%
import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

driver = webdriver.Chrome(options=options, service=Service(
    ChromeDriverManager().install()))

# Navigate to the jjalbot.com webpage
driver.get("https://jjalbot.com/random")


# Wait for the photo to load
photo = WebDriverWait(driver, 10).until(
    # EC.presence_of_element_located((By.CLASS_NAME, "h-full.w-full.rounded")),
    EC.presence_of_all_elements_located(
        (By.CLASS_NAME, "h-full.w-full.object-contain"))
)

# 아래 값들 비어 있으면 -> get_attribute title을 해시태그로 가져오고
# url -> 아래 source 값을 가져오기
urls = [element.get_attribute("src") for element in photo]
alts = [element.get_attribute("alt") for element in photo]
titles = [element.get_attribute("title") for element in photo]

print(titles)

total = zip(urls, alts)


for url in total:
    print("Photo URL:", url)


# Close the browser window
driver.quit()
