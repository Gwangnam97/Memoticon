import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


def crawl_naver_selenium(url: str) -> list:
    driver.get(url)

    # div 추출
    div = driver.find_elements(By.ID, "viewTypeSelector")[0]

    # img 추출
    img = div.find_elements(By.TAG_NAME, "img")
    url_list = []

    # return img
    for i in img:
        url_list.append(i.get_attribute("src"))

    return url_list


def crawl_naver(url: str) -> list:  # 블로그에서 이미지 url 추출
    # Requests 모듈 기본 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "lxml")

    # 모든 img 태그 의 src추출
    img_tags = soup.find_all("img")
    img_urls = [tag["src"] for tag in img_tags]

    # 이미지 형식 재정의
    url_list = []
    for urls in img_urls:
        if not urls.startswith("https://mblogthumb"):
            continue
        url_list.append(str(urls).split("_blur")[0] + "0")

    if len(url_list) < 10:  # requests 크롤링 안될 시 selenium 크롤링 진행
        return crawl_naver_selenium(url)

    return url_list if url_list else None  # 이미지가 없으면 None 반환


# selenium의 크롬드라이버 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("headless")
options.add_argument("window-size=1920x1080")
driver = webdriver.Chrome(
    options=options, service=Service(ChromeDriverManager().install())
)



# blog의 짤 post_url 추출
link = "https://m.blog.naver.com/wjddmswjd555/223023551908"
target_url_list = [link]

target_url_list.append("https://m.blog.naver.com/windysky70/222885936763")

# post 안에 img_url 추출 & create df
df = pd.DataFrame(columns=["img"])
for idx in target_url_list:
    img_list = crawl_naver(idx)
    if img_list:
        df_new = pd.DataFrame({"img": img_list})
        df = pd.concat([df, df_new], axis=0)


# 저장
local_path = r"C:\Users\Playdata\Desktop\Memoticon\blog\Gongbu.csv"
df.dropna(inplace=True)  # None 값을 가지는 레코드 삭제
df.to_csv(local_path, index=False, encoding="utf-8-sig")
print("Done!!!")