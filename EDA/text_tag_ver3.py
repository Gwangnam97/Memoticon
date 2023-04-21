import pandas as pd
import numpy as np
import pickle
import re
from tqdm import tqdm
from konlpy.tag import Hannanum, Komoran, Okt

# 데이터 통합
total_data = pd.read_csv('./2runjjal_fixed.csv')
total_data = pd.concat([total_data, pd.read_csv('./pinterest_fixed.csv.csv')])
total_data = pd.concat([total_data, pd.read_csv('./pinterest2.csv')])
total_data = pd.concat([total_data, pd.read_csv('./jjalbox_fixed.csv')])
total_data = pd.concat([total_data, pd.read_csv('./ppomppu_fixed.csv')])
total_data = pd.concat([total_data, pd.read_csv('./todaysjjalbang_fixed.csv')])
# 인덱스가 중복 되므로 인덱스 재정렬
total_data = total_data.reset_index().drop(columns = ['index'])
# 판다스로 불러오면 결측치가 NaN 이므로 None 값으로 변경
total_data = total_data.replace({np.nan: None})

# 해시태그 형식 통일 (띄어쓰기 없는 , 로 통일)
tmp = []
for i in range(len(total_data)):
    if total_data['hashtag'][i] == None:
        tmp.append(None)
    else:
        tmp.append(total_data['hashtag'][i].replace(' ',','))
total_data['hashtag'] = tmp

tmp = []
for i in range(len(total_data)):
    if total_data['hashtag'][i] == None:
        tmp.append(None)
    else:
        tmp.append(total_data['hashtag'][i].replace(',,',','))
total_data['hashtag'] = tmp

# 정규표현식 사용. text에 한글 영어 숫자 , . 빈칸만 남김
r = re.compile(r"[^ㄱ-ㅎ가-힣a-zA-Z0-9,.\s]")
tmp = []
for i in range(len(total_data)):
    if total_data['text'][i] == None:
        tmp.append(None)
    else:
        tmp.append(r.sub("", total_data['text'][i]))
total_data['text'] = tmp

# text 에서 중복된 글(4개 이상)은 태그화 하지 않을 예정이므로
# 4개 이상인 텍스트 목록 추출
del_text_lst = total_data.groupby('text').count()['url'].sort_values(ascending=False)[:1500].index

# Hannanum, Komoran 이용 명사 추출(외국어 포함)
# Okt 이용 형용사 동사 기본형 추출
#명사 동사 형용사 추출 하여 text_tag 에 저장
text_tag = []
for i in tqdm(range(len(total_data))):
    try:
        if total_data['text'][i] in del_text_lst or total_data['text'][i] == None:
            text_tag.append(None)
        else:
            tmp_tag = []
            for x,y in Hannanum().pos(total_data['text'][i],ntags=22):
                if y == 'NC' or y == 'F':
                    tmp_tag.append(x)
            for x,y in Komoran().pos(total_data['text'][i]):
                if y == 'NNP' or y == 'MAG' or y == 'NA':
                    tmp_tag.append(x)                    
            for x,y in Okt().pos(total_data['text'][i], norm=True, stem=True):
                if y == 'Adjective' or y == 'Verb':
                    tmp_tag.append(x)                          
            tmp_tag = list(set(tmp_tag))
            tmp_str = ','.join(tag for tag in tmp_tag)        
            text_tag.append(tmp_str)
    except:
        print( i ," 오류")
        text_tag.append(None)
        
    with open(f'tmp_text_tag_{i}.pkl','wb') as f: # 혹시 중간에 터질까봐 10000번째 마다 임시저장
        pickle.dump(text_tag, f)

# 이번 오류는 뭐지... => 한글 영어 숫자만 남겻을 때, 빈칸이 되면 오류가 뜸
# 61%, 62%에서 멈췄다가 한참 있다가 다시 되는 현상이 있음 97859,97952,98596 왜 그러지...

total_data['text_tag'] = text_tag

total_data.to_csv('./total_data_plus_text_tag_ver2.csv',index=False,encoding='utf-8')