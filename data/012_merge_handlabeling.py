import pandas as pd

df = pd.read_csv(r'C:\Memoticon\data\csv\data.tsv', sep='\t', encoding="utf-8-sig")
ddf = pd.read_csv(r'C:\Memoticon\data\csv\team_hand_labeling.csv', encoding="utf-8-sig")

ddf.loc[ddf['hashtag'] == 'x', 'hashtag'] = 'X'
ddf_x = ddf[ddf['hashtag'] == 'X']
ddf_hand = ddf[ddf['hashtag'] != 'X']

# X라고 표기한 데이터 삭제
df = df[~(df['url'].isin(ddf_x['url']))]


# ddf_hand 'url' 값이 df의 'url' 컬럼에 있는 경우 해당 값을 df의 'hashtag' 컬럼에 넣어줌
for index, row in ddf_hand.iterrows():
    if row['url'] in df['url'].values:
        df.loc[df['url'] == row['url'], 'hashtag'] = row['hashtag']

df.to_csv(r'C:\Memoticon\data\csv\data.tsv', sep='\t', encoding="utf-8-sig", index=False)
# # 결과 확인
# print(df)
