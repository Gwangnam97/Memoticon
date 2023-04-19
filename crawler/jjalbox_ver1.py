import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from tqdm import tqdm
#7434 까지 있음


# 데이터 저장할 jjalbox 폴더 만들어야 함.


tmp_lst = []

# 짤박스 웹페이지 143201 번 부터 내림차순으로 크롤링
# 115000 번까지 지금 형식 그 다음부터는 ver.2 로 돌릴것.
for i in tqdm(range(143201,115000,-1)):
    # 혹시 모를 try except
    try:
        # 짤박스 링크 1은 페이지 인데 숫자 상관X , 맨 뒤 '/' 빼면 오류 뜸
        page = requests.get(f"https://jjalbox.com/view/free/1/{i}/")
        soup = bs(page.text, "html.parser")

        # 필요한 데이터 받을 변수 생성
        # 제목 과 본문은 텍스트만 받음
        title = soup.select('div.info h4 > span')[0].get_text()
        img = None
        video = None
        text = soup.select('article.text')[0].get_text()

        # 사진이 있을 시, 모든 이미지url 을 리스트에 넣음
        if "img" in page.text:
            imgall = soup.findAll('figure')
            imglst = []
            for ia in imgall:
                if "img" not in str(ia): # figure 를 받다 보니 img 만 뽑을수 없음. video 등 섞여 있을경우 오류 -> img 가 아닐 경우 pass
                    pass
                else:
                    imglst.append(ia.find("img")["src"])
            img = imglst
        # 동영상이 있을 시, 모든 동영상 url 리스트에 넣음
        if "video" in page.text:
            videoall = soup.findAll('video')
            videolst = []
            for va in videoall:
                videolst.append(va.find("source")["src"])
            video = videolst
        # 하나의 리스트로 통합
        tmp_lst.append([title, img, video, text])
    except:
        print(i, " 오류")
    if i % 5000 ==1:
        # 5천개씩 csv 파일로 저장.
        pd.DataFrame(tmp_lst, columns= ['title','img','video','text']).to_csv(f"./jjalbox/jjalbox_{i//5000}.csv",index=False) #숫자가... 내림차순임..ㅎ....ㅈㅅ
        tmp_lst = [] # tmp_lst 초기화

