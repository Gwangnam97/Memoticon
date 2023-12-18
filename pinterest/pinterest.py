import pandas as pd
import numpy as np
from konlpy.tag import Okt
okt = Okt()

pinterest = pd.read_excel("./pinterest.xlsx")

# title 내 필요한 부분 추출
for idx, value in enumerate(pinterest.title):
    if "|" in str(value):
        pinterest.title[idx] = value.split("|")[-1]
    elif value == "":
        pinterest.title[idx] = "NaN"


# description 내 필요한 부분 추출
for idx, value in enumerate(pinterest.description):
    if "|" in str(value):
        pinterest.description[idx] = value.split("|")[-1]
    elif value == "":
        pinterest.description[idx] = "NaN"
        
# title, description 합치기 
tmp = []
for i,j in zip(pinterest["title"], pinterest["description"]):
        tmp.append(str(i) + "/" + str(j))
tmp = [text.replace("nan", "") for text in tmp]

text = []
for v in tmp:
    if v == "/":
        text.append(None)
    elif v.startswith("/") or v.endswith("/"):
        text.append((v.replace("/","")).lstrip(" "))
    else:
        text.append(v)
        

# 컬럼생성, 삭제
pinterest['text'] = text
pinterest["hashtag"] = None
pinterest['crawled_at'] = "pinterest"
pinterest.drop(columns=["title", "description"], axis=1, inplace=True)

# 파일저장
pinterest.to_csv("./pinterest_fixed2.csv", index=False)