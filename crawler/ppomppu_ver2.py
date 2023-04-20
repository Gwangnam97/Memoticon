import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm
import time

tmp_lst = []
# 뽐뿌 9번 부터 있음
# 52325 까지

#저장될 폴더 만들어야 함. 이거 필수 !!!!

# 시간 간격 안두니 웹페이지가 터져서 ... 0.2초 간격

#최신부터 내림차순으로 크롤링
for i in tqdm(range(50000,25000,-1)):
    time.sleep(0.2)
    # 혹시 모를 try except
    try:
        # 사이트가 정말 편하게 되어 있음. 링크 뒷자리만 바꾸면 됨
        page = requests.get(f"https://www.ppomppu.co.kr/zboard/view.php?id=jjalbang&no={i}")
        soup = bs(page.text, "html.parser")
        #meta 데이터에 필요한게 다 있음. 순서가 고정이라 7번=제목, 9번=url
        #tag 가 # 붙어서 나옴. 제일 앞에 빈칸이 있음.ㅠ
        title = soup.select('meta')[7]['content']
        url = soup.select('meta')[9]['content']
        tag = soup.select('div.sub-top-text-box > b')[0].get_text()
        tmp_lst.append([title, url, tag, i])
    except:
        print(i, " 오류")
    if i % 5000 ==1:
        # 5천개씩 csv 파일로 저장.
        pd.DataFrame(tmp_lst, columns= ['title', 'url', 'tag','number']).to_csv(f"./ppomppu/ppomppu_{i//5000}.csv",index=False) #숫자가... 내림차순임..ㅎ....ㅈㅅ
        tmp_lst = [] # tmp_lst 초기화