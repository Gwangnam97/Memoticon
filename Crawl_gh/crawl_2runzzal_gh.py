# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
driver = webdriver.Chrome(options=options, service=Service(
    ChromeDriverManager().install()))

driver.get("https://2runzzal.com/?lang=ko")


# 스크롤을 끝까지 내리는 작업을 반복
last_height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)  # 페이지 로드 대기시간
    new_height = driver.execute_script('return document.body.scrollHeight')
    if new_height == last_height:
        break
    last_height = new_height


div = driver.find_elements(By.CLASS_NAME, 'relative ')

# save to csv
df = pd.DataFrame(columns=["url", "tag"])

for i in list(range(len(div))):
    # find elements
    target_div = div[i]

    try:
        url = target_div.find_element(
            By.CLASS_NAME, 'lazy').get_attribute("data-filename")
    except:
        continue
    tag = target_div.find_elements(By.CLASS_NAME, 'zzal-info-tag')
    tag_list = []

    for tag in tag:
        tag_list.append(tag.get_attribute("innerHTML"))

    # Get the index of the last row
    df.loc[len(df)] = [url, tag_list]

df.to_csv('./2runzzal.csv')

driver.quit()

# %%
