import pandas as pd
import concurrent.futures
import requests
from PIL import Image
from io import BytesIO


# 이미지의 가로와 세로 비율을 확인하는 함수
def get_image_ratio(url):
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        ratio = image.width / image.height
        return ratio
    except:
        print(f"Failed to open image at URL: {url}")
        return 0


# 비동기적으로 작업을 처리하는 함수
def process_urls(df):
    urls = df["url"].tolist()
    results = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # 이미지 비율을 확인하고 삭제 대상을 식별
        for url, ratio in zip(urls, executor.map(get_image_ratio, urls)):
            print(f"ratio : {ratio}, {url}")
            if ratio < 0.6:
                results.append(url)

    # 삭제 대상을 DataFrame에서 제거
    filtered_df = df[~df["url"].isin(results)]
    return filtered_df


def main():
    df = pd.read_csv(r"C:\Memoticon\data\006_drop_by_ratio.csv", encoding="utf-8-sig")
    # df = df.head(300)
    # # 비동기 작업 수행
    filtered_df = process_urls(df)
    print(filtered_df)
    filtered_df.to_csv("./test.csv", index=False)


if __name__ == "__main__":
    main()
