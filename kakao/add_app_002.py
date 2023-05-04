from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
import uvicorn

import aiomysql
from pydantic import BaseModel
# MySQL connection configuration
config = {
    "host": "52.78.88.87",
    "user": "root",
    "password": "1234",
    "database": "sys",
    "port": "54978",
}
main_table = "sys.main"


# 데이터 모델
class Data(BaseModel):
    id: int
    url: str
    hashtag: str



# Create a connection pool with 5 connections
async def get_data_from_database():
    global cached_data
    async with aiomysql.create_pool(**config) as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                query = f"SELECT id, url, hashtag FROM {main_table} LIMIT 5"
                await cursor.execute(query)
                results = await cursor.fetchall()
    cached_data = [Data(id=row[0], url=row[1], hashtag=row[2]) for row in results]


# 캐시 데이터 업데이트
def update_cached_data():
    global cached_data
    cached_data = get_data_from_database()

# 백그라운드 태스크
def update_cache_data_task():
    update_cached_data()
# Create FastAPI app instance
app = FastAPI()

# 스케줄러 대신 백그라운드 태스크 사용
@app.on_event("startup")
async def startup_event():
    update_cache_data_task()

# API 엔드포인트
@app.get("/", response_model=List[Data])
async def get_data():
    return cached_data


# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)

