import pandas as pd

df = pd.read_csv(
    r'C:\Memoticon\001_remain_url_status_is_200.csv', index_col=[0])

# 쓰레기 버리기
df = df[df["text"] != "삭제되었거나,비공개된,게시물입니다."]
df = df[df["text"] != " 피클포털 1 페이지김레알의 피드클릭, 유머짤방 큐레이션 서비스 제공"]

df = df[df["url"] != "https://www.ppomppu.co.kr/images/icon_app_20160427.png"]
# df = df[df["hashtag"] != ""]

df.drop_duplicates(subset=['url'], inplace=True)


df.to_csv('002_drop_garbage_data.csv')
print("DONE")


