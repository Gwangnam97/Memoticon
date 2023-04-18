# %%
import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

# Requests 모듈 기본 설정
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

# 기본 인코딩이 utf-8이 아닌 경우 설정
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# 데이터프레임 생성
df = pd.DataFrame(columns=["thumbnail", "origin", "tag"])

# 저장할 CSV 파일 경로
CSV_FILE_PATH = "./Crawl_gh/ppomppu.csv"

# 크롤링할 URL 범위
url_range = range(1, 2356)
# url_range = range(62, 64)


for page_num in url_range:
    url = f'https://www.ppomppu.co.kr/zboard/zboard.php?id=jjalbang&page={page_num}&divpage=10'
    print(url)

    # HTML 파싱
    soup = BeautifulSoup(requests.get(url, headers=headers).text, "lxml")

    # 이미지와 태그 추출 후 데이터프레임에 추가
    td_tags = soup.find_all("td", {"valign": "top"})

    for td in td_tags:
        thumbnail = td.find("img", {"onfocus": "blur()"})['src']
        tag = td.find("font", {"class": "thumb_list_title"}).get_text()

        target_url = 'https://www.ppomppu.co.kr/zboard/' + \
            td.find("a", {"onfocus": "blur()"})['href']
        soup_target = BeautifulSoup(requests.get(
            target_url, headers=headers).text, "lxml")
        td_target = soup_target.find("td", {"class": "board-contents"})

        if len(td_target.find_all("video")) >= 1:  # GIF
            origin = td_target.find("source")['src']
        elif len(td_target.find_all("img")) >= 1:
            origin = list(i['src'] for i in td_target.find_all("img"))

        df.loc[len(df)] = ["https:" + thumbnail, origin, tag]

        # 데이터프레임 출력 및 CSV 파일로 저장
df.to_csv(CSV_FILE_PATH, index=False)
print("Done!!")
