#%%
import requests
import pandas as pd
from PIL import Image
import io

df = pd.read_csv(r'C:\Memoticon\data\005_after_cleaning.csv')
df.fillna("X", inplace=True)


def filter_images(row):  # 이미지 필터링 함수
    url = row['url']
    response = requests.head(url)
    print(response, url)  # HEAD 요청을 통해 HTTP 상태 코드 확인

    if url.endswith(('jpg', 'png', "jpeg", "webp")) and response.status_code == 200:
        image_data = requests.get(url).content
        try:
            image = Image.open(io.BytesIO(image_data))
        except:
            return None
        width, height = image.size

        # 가로에 비해 세로가 긴 이미지 제거
        # https://andrew.hedges.name/experiments/aspect_ratio/
        if (width * 10) <= (height * 5):
            return None

    return row


# 이미지 필터링 적용 & fillna 처리
df_filtered = df.apply(filter_images, axis=1).dropna()
#%%
df.loc[df['hashtag'] == "X", 'hashtag'] = ""

# 결과 확인
df_filtered.to_csv('./006_drop_by_ratio.csv', index=False)
