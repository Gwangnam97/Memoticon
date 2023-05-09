import os
import random
import openai
import aiomysql
import asyncio
import aiohttp
import uvicorn

from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import tracemalloc

tracemalloc.start()

# Initialize the FastAPI app
app = FastAPI()


# Define the database connection configuration
config = {
    "host": "52.78.88.87",
    "port": 54978,
    "user": "root",
    "password": "1234",
    "db": "sys",
}
cache_data = (
    (1, "http://example.com", "cat,dog"),
    (2, "http://example.net", "dog"),
    (3, "http://example.org", "cat,elephant"),
)

# 각 데이터의 answer 포함 개수를 계산하는 함수
async def count_category(data, category_names):
    count = sum(1 for name in category_names if name in data[2].split(","))
    return count

answer = ["dog", "cat","elephant"]

@app.on_event("startup")
async def on_startup():
    print("SERVER STARTUP")

    max_count = 0
    meme_cache = []

    for data in cache_data:
        count = await count_category(data, answer)
        if count > max_count:
            max_count = count
            meme_cache = [data]
        elif count == max_count:
            meme_cache.append(data)

    print(f'meme_cache : {meme_cache[:3]}')
    return tuple(meme_cache)


# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)

