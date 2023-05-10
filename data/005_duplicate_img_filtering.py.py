import pandas as pd

df = pd.read_csv(r'C:\Memoticon\data\004_word_filtering.csv', index_col=[0])

# NaN 값을 빈 문자열로 대체
df['hashtag'].fillna('', inplace=True)

# 'url' 컬럼을 쉼표(,)로 분할하고 분할된 리스트의 길이를 'url_len' 컬럼에 저장
df['url_len'] = df['hashtag'].str.split(',').apply(lambda x: len(x))

# 'url_len'이 2 이하인 경우를 1로, 그렇지 않은 경우를 0으로 변환
df['url_len'] = df['url_len'].apply(lambda x: 1 if x <= 2 else 0)

# 1은 ocr 필요, 0은 불필요
df.to_csv('add_tag_for_ocr.csv', index=False)
