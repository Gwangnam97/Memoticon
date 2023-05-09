import cv2
import aiohttp
import asyncio
import pandas as pd
from pororo import Pororo

async def download_image(session, url, index):
    async with session.get(url) as response:
        data = await response.read()
        with open(f"temp_image_{index}.jpg", "wb") as f:
            f.write(data)

async def ocr_with_pororo(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ocr = Pororo(task="ocr", lang="ko")
    results = ocr(gray)
    print(results)
    return " ".join(results)

async def process_row(session, row):
    image_url = row.url
    index = row.Index
    await download_image(session, image_url, index)
    image_path = f"temp_image_{index}.jpg"
    ocr_result = await ocr_with_pororo(image_path)
    return ocr_result

async def process_data(data):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for row in data.itertuples():
            task = asyncio.create_task(process_row(session, row))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
    return results

# CSV 파일을 읽어옵니다.
data = pd.read_csv("semi_data.csv")
data = data.head()

# 비동기 작업을 실행하여 OCR 결과를 추출합니다.
loop = asyncio.get_event_loop()
ocr_results = loop.run_until_complete(process_data(data))

# 결과를 데이터프레임에 할당합니다.
data["ocr_result"] = ocr_results

# 결과를 출력합니다.
print(data)
