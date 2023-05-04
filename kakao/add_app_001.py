#%%
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
import uvicorn
import mysql.connector.pooling

# MySQL connection configuration
config = {
    "host": "52.78.88.87",
    "user": "root",
    "password": "1234",
    "database": "sys",
    "port": "54978",
}

# Define tables & columns, Delete & save rows to del_history
main_table = "sys.main"


# 데이터 모델
class Data(BaseModel):
    id: int
    url: str
    hashtag: str


# 캐시 데이터 저장소
cached_data = []

# Create MySQL connection pool
connection_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="my_pool", pool_size=5, **config
)


# 데이터베이스에서 crawl_data 가져와서 캐싱
def get_data_from_database():
    with connection_pool.get_connection() as conn:
        cursor = conn.cursor()

        query = f"SELECT id, url, hashtag FROM {main_table} LIMIT 12"
        cursor.execute(query)
        results = cursor.fetchall()

    return [Data(id=row[0], url=row[1], hashtag=row[2]) for row in results]


# 캐시 데이터 업데이트
def update_cached_data():
    global cached_data
    cached_data = get_data_from_database()


# Create FastAPI app instance
app = FastAPI()


# API 엔드포인트
@app.get("/", response_model=List[Data])
async def get_data():
    return cached_data


# 백그라운드 태스크
def update_cache_data_task():
    update_cached_data()


# 스케줄러 대신 백그라운드 태스크 사용
@app.on_event("startup")
async def startup_event():
    update_cache_data_task()

    # 스케줄러 대신 백그라운드 태스크 사용
    background_tasks = BackgroundTasks()
    background_tasks.add_task(update_cache_data_task)
    app.background_tasks = background_tasks


# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)



#%%
import time
import schedule

@app.on_event("startup")
async def startup_event():
    update_cache_data_task()
    background_tasks = BackgroundTasks()
    background_tasks.add_task(update_cache_data_task)
    app.background_tasks = background_tasks

def update_cache_data_task():
    # 실행될 함수 내용 작성
    print("Cache data updated")

def scheduled_task():
    schedule.every(1).hour.do(update_cache_data_task)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    # 서버가 켜질 때 실행될 함수
    startup_event()

    # 1시간 간격으로 실행될 함수
    scheduled_task()

if __name__ == "__main__":
    main()
