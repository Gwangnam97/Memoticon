import pandas as pd
import asyncio
import aiohttp

# DataFrame 생성 (예시)
df = pd.read_csv(r'C:\Memoticon\data\data_origin.csv')

# HTTP 상태 코드 확인 함수 정의 (비동기)
async def check_status(session, url):
    try:
        async with session.head(url) as response:
            return response.status == 200
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return False

# 비동기로 DataFrame 업데이트
async def update_dataframe(df):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in df['url']:
            print(f'url in progress : {url}')
            task = check_status(session, url)
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        df = df[results]
        return df

# 비동기 업데이트 함수 실행
loop = asyncio.get_event_loop()
updated_df = loop.run_until_complete(update_dataframe(df))

# DataFrame을 CSV 파일로 저장
updated_df.to_csv('001_remain_url_status_is_200.csv')
print("DONE_URL_CHECK")