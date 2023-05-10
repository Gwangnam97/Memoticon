import pandas as pd

# df = pd.read_csv(r'C:\Memoticon\002_drop_garbage_data.csv',index_col=[0])
df = pd.read_csv(r'C:\Memoticon\data\003_hand_cleaning.csv',index_col=[0])


# ,기준으로 나누고 몇개있는지 확인
# df['hashtag_len'] = df['hashtag'].str.split(',').apply(lambda x: len(x))
"""
1. text+hashtag+text_tag 병합하는 과정
, 로 시작하는 값의 맨 앞 , 삭제
다수의 "피클XX 1 페이지" 값 삭제
    ㄴ 다수의 "피클포털 1 페이지김레알의 피드클릭, 유머짤방 큐레이션 서비스 제공" 값 삭제
다수의 "ppom" 값 삭제
다수의 "루리웹 루리웹 모바일" 값 삭제
다수의 "HugeDomains" 값 삭제
다수의 ".com" 값 삭제
다수의 "http" 값 삭제
다수의 "Pin on 빠른 저장" 값 삭제
다수의 "보다 보면 짠해지는, 직장인 공감 일러스트 30선최근 직장인들 사이에서 격한 공감을 사고 있는 일러스트가 있다. 양경수 작가가 그림왕 양치기라는 필명으로 자신의 페이스북 페이지 약치기 그림페이스북 바로가기에 올리는 그림들이다. 해당 일러스트는 직장인 애환을 유쾌하게 그려냈다는 평을 듣고 있다. 그의 삽화는 최근 책 아, 보람 따위 됐으니 야근수당이나 주세요, SBS 스페셜 요즘 젊은 것들의 사표 등에도 나오며 주목을 받기도 했다. 보람따위 됐으니 야근수당이나 신간 SNS서 화제wikitree.co.kr 화제의 신간을 곤님에게 전해받았다.최근 SNS에서 많은 공감을 사고 있는 작가의 일러스트를 모았다. 1. 눈치 없는 녀석이하 페이스북 페이지 약치기 그림 작가 동의 하 게재 2. 전생에 업이 많아 업무가 UP됐구나 3. 일하기싫어증 4. 하기싫음 장인 5. 그냥 가만" 값 삭제
다수의 "원덬 감성취향의 핀터레스트 짤 모음 스퀘어 카테고리원덬 감성취향의 핀터레스트 짤 모음 스퀘어 카테고리" 값 삭제

hashtag 의 빈값은 크롤할 때 게시물의 디스크립션 값이 있다면 해당 값으로 대체 : 서버에서 키워드 찾을 때 "in" 으로 찾기 때문에 , 로 나누지 않아도 기능상 큰 문제 없음
hashtag 컬럼의 null 이 아닌 값 중에 기호만 들어있다면 디스크립션값으로 대체, 나머지 기호만 있는 값은 삭제
�� <- 유니코드가 포함된 있는 단어만 삭제 : hashtag 전체 삭제 아님
1 글자 
"""

df['hashtag'].value_counts().to_csv('./003_hand_cleaning_hashtag_value_counts.csv')