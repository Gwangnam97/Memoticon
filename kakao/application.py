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

# Define blocks ID
block_id_send_img_random = "644a0944b5e5636c2125a14c"
block_id_send_img = "64477498d853bb56940a87bd"
block_id_meme = "6445fd79d853bb56940a7c49"


# Define the database connection configuration
config = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "1234",
    "db": "sys",
}


# Define tables & columns, Delete & save rows to del_history
main_table = "sys.main"
del_table = "sys.del_history"
count_column = "count_sum"
target_column = "hashtag"

meme_cache = None
answer = None

gpt_dead_massage = "Mememo dead now...😰🌡"
default_fallback_massage = "데이터가 없습니다."


async def fallback_massage(massage):
    # Fallback message format
    fallback_res = {
        "version": "2.0",
        "template": {
            "outputs": [{"simpleText": {"text": massage}}],
            "quickReplies": quick_replies,
        },
    }
    return fallback_res


async def create_pool():  # Function: Create a coroutine to create a database connection pool
    print("creating pool")
    global pool
    pool = await aiomysql.create_pool(**config)


async def init_cache():  # Function: Create a coroutine to initialize the cache with *data from the database
    print("start init_cache")
    global cache_data
    global range_all_data
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            # Execute a SELECT statement to retrieve all rows from the "main" table
            await cur.execute("SELECT * FROM main;")
            # Store the fetched rows in the cache_data variable
            cache_data = await cur.fetchall()
            range_all_data = range(len(cache_data))
            # id = cache_data[i][0]
            # hashtag = cache_data[i][2]
            # url = cache_data[i][1]
            print(f"done init_cache")


async def url_check(check_data):  # Function: url check
    items = []

    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            try:
                # Set timeout to None
                timeout = aiohttp.ClientTimeout(total=None)
                async with aiohttp.ClientSession(timeout=timeout) as session:
                    # Send a HTTP request to the image URL
                    async with session.get(check_data[1]) as response:
                        # Check status code and delete the failed URL
                        if response.status != 200:
                            await cur.execute(
                                f"DELETE FROM {main_table} WHERE url = '{check_data[1]}'"
                            )
                            await cur.execute(
                                f"INSERT IGNORE INTO {del_table} (img_id, url, hashtag) VALUES (%s,%s,%s)",
                                (check_data[0], check_data[1], check_data[2]),
                            )
                            await conn.commit()
                        else:
                            # Add the URL to the list of items
                            items.append(
                                {
                                    "thumbnail": {
                                        "imageUrl": check_data[1],
                                        "fixedRatio": True,
                                        "link": {"web": check_data[1]},
                                    },
                                    "buttons": [
                                        {
                                            "action": "share",
                                            "label": "공유하기",
                                            "messageText": "공유하기",
                                        }
                                    ],
                                }
                            )
            except aiohttp.ClientError:
                pass

    return items


async def get_quick_replies():  # Function: Create a coroutine to initialize the cache with quick_replies_data from the database
    print("start get_quick_replies")
    global quick_replies_labels
    global quick_replies

    # async with pool.acquire() as conn:
    #     async with conn.cursor() as cur:
    #         # Extract the most popular keywords
    #         query = f"SELECT SUBSTRING_INDEX(SUBSTRING_INDEX({target_column}, ',', n), ',', -1) AS tag_word, COUNT(*) AS cnt FROM {main_table} CROSS JOIN (SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10) AS nums WHERE n <= 1 + LENGTH({target_column}) - LENGTH(REPLACE({target_column}, ',', '')) GROUP BY tag_word ORDER BY cnt DESC LIMIT 6;"
    #         await cur.execute(query)
    #         popular_keywords = await cur.fetchall()
    #         # Store the fetched rows in the range_all_data variable
    #         quick_replies_labels = [result[0] for result in popular_keywords]

    #         print(f'quick_replies_labels : {quick_replies_labels}')
    #         print(f'type(quick_replies_labels) : {type(quick_replies_labels)}')
    quick_replies_labels = ['행복', '슬픔', '황당',
                            '짜증', '분노', '놀림', '축하', '감사', '무한도전']

    # Quick replies format
    quick_replies = [
        {
            "label": label,
            "action": "block",
            "blockId": block_id_send_img,
            "extra": {"name": label},
        }
        for label in quick_replies_labels
    ]

    print("done get_quick_replies")


# Function: Create a coroutine to perform a keyword search on the cached data
async def query_keyword(keyword: str):
    # Search the cached data for the keyword
    result = [
        [entry[0], entry[1], entry[2]]for entry in cache_data if keyword in entry[2]]
    return result


async def update_cache_every_hour():  # Function: Create a coroutine to update the cache every hour
    print("start update_cache_every_hour")
    while True:
        # Reinitialize the cache with quick replies data from the database
        await init_cache()
        await get_quick_replies()
        print("SERVER IS READY")
        # Wait for 3600 seconds before updating the cache again
        await asyncio.sleep(3600)


# Function: Get category name from the request
async def get_category_name(req: dict) -> str:
    return req.get("action", {}).get("clientExtra", {}).get("name", "Read_Error!!!")

# Function: Get category name from the request


async def get_meme_cache_exist(req: dict) -> str:
    return req.get("action", {}).get("clientExtra", {}).get("meme_cache", None)


# Function: Send image response with data
async def send_img_res(
    items: list, block_id: str, category_name: str = "무작위", meme_cache: str = "None"
) -> JSONResponse:
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": f"{category_name}의 밈을 추천해드립니다. "
                        "더 많은 밈을 보고싶은 경우 아래의 더보기를 눌러주세요",
                        "buttons": [
                            {
                                "action": "block",
                                "label": "더보기",
                                "blockId": block_id,
                                "extra": {"name": category_name, "meme_cache": meme_cache},
                            }
                        ],
                    }
                },
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": items,
                    }
                },
            ],
            "quickReplies": quick_replies,
        },
    }

    return JSONResponse(content=res)


# Function: Get the image data from MySQL database
async def get_image_data(category_name: str = "무작위"):
    # Images to be sent to Kakao & Ad-hoc search algorithm
    if category_name == "무작위":
        random_list = random.sample(range_all_data, k=len(range_all_data))
        items = []

        for i in random_list:
            if len(items) == 3:
                return items

            items.extend(await url_check(cache_data[i]))

    elif category_name != "무작위":
        items = []
        result = await query_keyword(category_name)
        random_list = random.sample(result, k=len(result))
        for i in random_list:
            if len(items) == 3:
                return items
            items.extend(await url_check(i))

    return items


# Function: Get keyword from gpt
async def get_keyword_with_gpt(input_sentence: str) -> list:
    # Set up an API key to access the OpenAI API
    openai.api_key = os.getenv("api_key")
    # Extract key words from sentences using the GPT-3 model
    messages = [
        {"role": "user",
            "content": f"아래 문장에서 핵심단어를 3개만 추출해주세요. \n\n {input_sentence}"}
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0.2
    )
    category_name = completion.choices[0].message.content

    # Convert the extracted words into a list
    category_lists = category_name.split(", ")
    category_list = [category.rstrip(".") for category in category_lists]

    return category_list


# 각 데이터의 answer 포함 개수를 계산하는 함수
async def count_category(data, category_names):
    count = sum(1 for name in category_names if name in data[2].split(","))
    return count


@app.on_event("startup")
async def on_startup():  # Register an event handler to create a database connection pool when the app starts up
    print("SEVER STARTUP")
    await create_pool()
    # Register the update_cache_every_hour coroutine with the asyncio event loop
    asyncio.ensure_future(update_cache_every_hour())


# Route: Recommend images
@app.post("/recommend")
async def recommend(request: Request):
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": "✨추천 도와드릴게요!\n☝우선 어떻케 추천해줄지 정해볼까요?"}},
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "description": "어떤 상황에서 사용할건지 선택하기",
                                "thumbnail": {
                                    "imageUrl": "https://i.ibb.co/ZgTbB5R/choose-keyword.png"
                                },
                                "buttons": [
                                    {
                                        "action": "message",
                                        "label": "키워드 선택하기",
                                        "messageText": "키워드 선택하기",
                                    }
                                ],
                            },
                            {
                                "description": "문장을 입력하고 밈을 추천 받아보기",
                                "thumbnail": {
                                    "imageUrl": "https://i.ibb.co/6gwk09r/input-sentense.png"
                                },
                                "buttons": [
                                    {
                                        "action": "message",
                                        "label": "밈모에게 얘기하기",
                                        "messageText": "밈모에게 얘기하기",
                                    }
                                ],
                            },
                        ],
                    }
                },
            ]
        },
    }

    return JSONResponse(content=res)


# Route: Choose_keyword images
@app.post("/choose_keyword")
async def choose_keyword(request: Request):
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": "🌈추천 도와드릴게요!\n📌아래에서 키워드를 선택해주세요!"}},
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": "추천받을 키워드를 선택해주세요.",
                                "thumbnail": {
                                    "imageUrl": "https://i.ibb.co/Yjr07h8/keyword.png"
                                },
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": quick_replies_labels[0],
                                        "blockId": block_id_send_img,
                                        "extra": {"name": quick_replies_labels[0]},
                                    },
                                    {
                                        "action": "block",
                                        "label": quick_replies_labels[1],
                                        "blockId": block_id_send_img,
                                        "extra": {"name": quick_replies_labels[1]},
                                    },
                                    {
                                        "action": "block",
                                        "label": quick_replies_labels[2],
                                        "blockId": block_id_send_img,
                                        "extra": {"name": quick_replies_labels[2]},
                                    },
                                ],
                            },
                            {
                                "title": "추천받을 키워드를 선택해주세요.",
                                "thumbnail": {
                                    "imageUrl": "https://i.ibb.co/Yjr07h8/keyword.png"
                                },
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": quick_replies_labels[3],
                                        "blockId": block_id_send_img,
                                        "extra": {"name": quick_replies_labels[3]},
                                    },
                                    {
                                        "action": "block",
                                        "label": quick_replies_labels[4],
                                        "blockId": block_id_send_img,
                                        "extra": {"name": quick_replies_labels[4]},
                                    },
                                    {
                                        "action": "block",
                                        "label": quick_replies_labels[5],
                                        "blockId": block_id_send_img,
                                        "extra": {"name": quick_replies_labels[5]},
                                    },
                                ],
                            },
                            {
                                "title": "추천받을 키워드를 선택해주세요.",
                                "thumbnail": {
                                    "imageUrl": "https://i.ibb.co/Yjr07h8/keyword.png"
                                },
                                "buttons": [
                                    {
                                        "action": "block",
                                        "label": quick_replies_labels[6],
                                        "blockId": block_id_send_img,
                                        "extra": {"name": quick_replies_labels[6]},
                                    },
                                    {
                                        "action": "block",
                                        "label": quick_replies_labels[7],
                                        "blockId": block_id_send_img,
                                        "extra": {"name": quick_replies_labels[7]},
                                    },
                                    {
                                        "action": "block",
                                        "label": quick_replies_labels[8],
                                        "blockId": block_id_send_img,
                                        "extra": {"name": quick_replies_labels[8]},
                                    },
                                ],
                            },
                        ],
                    }
                },
            ]
        },
    }

    return JSONResponse(content=res)


# Route: Send images based on category
@app.post("/send_img")
async def send_img(request: Request):
    global meme_cache

    req = await request.json()
    print(req)

    is_exist_meme_cache = await get_meme_cache_exist(req)
    print(f'is_exist_meme_cache : {is_exist_meme_cache}')

    fallback_res = await fallback_massage(default_fallback_massage)

    # Select category
    category_name = await get_category_name(req)
    print(f'category_name : {category_name}')
    items = []

    if is_exist_meme_cache == None:
        print("meme_cache is not exist")
        items = await get_image_data(await get_category_name(req))
        if len(items) == 0:
            return JSONResponse(content=fallback_res)

        return await send_img_res(items, block_id_send_img, category_name, "exist")

    else:
        print("meme_cache is exist")
        random_list = random.sample(meme_cache, k=len(meme_cache))
        for i in random_list:
            if len(items) == 3:
                break
            items.extend(await url_check(i))

        if len(items) == 0:
            return JSONResponse(content=fallback_res)
        print(f"meme_cache items : {items}")
        return await send_img_res(items, block_id_send_img, category_name, "exist")


# Route: Send random images
@app.post("/send_img_random")
async def send_img_random(request: Request):
    items = await get_image_data()

    return await send_img_res(items, block_id_send_img_random)


gpt_dead_massage = "Mememo dead now...😰🌡"

# Route: Extract keyword and send images


@app.post("/talk_to_mememo")
async def talk_to_mememo(request: Request):
    req = await request.json()
    print(req)
    global meme_cache
    global answer

    # word_limit : 32767 | 32767byte
    input_sentence = req["action"]["detailParams"]["contents"]["origin"]

    # Catching GPT-request limit errors
    try:
        answer = await get_keyword_with_gpt(input_sentence)
        print(f'gpt_answer : {answer}')
    except Exception as e:
        print(f'Mememo dead now... Exception : {e}')
        return JSONResponse(content=await fallback_massage(gpt_dead_massage))

    # Convert cache_data tuple into an asynchronous iterable
    # 가장 높은 count 값 계산
    max_count = 0
    meme_cache = []
    for data in cache_data:
        count = await count_category(data, answer)
        if count > max_count:
            max_count = count
            meme_cache = [data]
        elif count == max_count:
            meme_cache.append(data)
    meme_cache = tuple(meme_cache)
    print(f'sample meme_cache : {meme_cache[:5]}')
    items = []
    random_list = random.sample(meme_cache, k=len(meme_cache))
    for i in random_list:
        if len(items) == 3:
            break
        items.extend(await url_check(i))

    if len(items) == 0:
        return JSONResponse(content=await fallback_massage(default_fallback_massage))

    category_name = ""
    for i in answer:
        category_name += i

    return await send_img_res(items, block_id_send_img, category_name, meme_cache="exist")


# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
