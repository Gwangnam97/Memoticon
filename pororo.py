import cv2
import urllib.request
from pororo import Pororo
import pandas as pd
df = pd.read_csv(r'C:\Memoticon\data\before_ocr_data.csv')

tmp  = (df['url'][3232])


def ocr_with_pororo(image_url):
    # 이미지를 다운로드합니다.
    urllib.request.urlretrieve(image_url, "temp_image.jpg")

    # 이미지 파일을 읽어옵니다.
    image = cv2.imread("temp_image.jpg")

    # 이미지를 그레이스케일로 변환합니다.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Pororo의 OCR 모듈을 초기화합니다.
    ocr = Pororo(task="ocr", lang="ko")

    # 이미지에서 텍스트를 추출합니다.
    results = ocr(gray)

    # 추출된 텍스트를 출력합니다.
    for result in results:
        print(result)

# 이미지 URL을 지정하여 함수를 호출합니다.
ocr_with_pororo(tmp)