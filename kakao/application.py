import uvicorn
import mysql.connector
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import requests
import openai
import os
import random

# from dotenv import load_dotenv

# load_dotenv()  # .env 파일에서 API 키를 불러옴

# 이미지 url != 200 인것들 리스트에 담아서 나중에 처리
# 즉 이미지를 전송 완료한 후에 깨진_이미지_리스트 를 DB에서 삭제 후 history에 저장
# modify del_history !!!
# modify del_history !!!
# get_image_data rand parameter 수정해!!!
# get_image_data rand parameter 수정해!!!

app = FastAPI()

# Define blocks ID
block_id_send_img_random = "644a0944b5e5636c2125a14c"
block_id_send_img = "64477498d853bb56940a87bd"


# MySQL connection configuration
config = {"host": "localhost", "user": "root", "password": "1234", "database": "sys"}

# Define tables & columns, Delete & save rows to del_history
main_table = "sys.main"
del_table = "del_history"
count_column = "count_sum"
target_column = "hashtag"

# Connect to MySQL
with mysql.connector.connect(**config) as conn:
    cursor = conn.cursor()

    # Extract the length of talbe
    query = f"SELECT * FROM {main_table}"
    cursor.execute(query)
    fetch_data = cursor.fetchall()
    range_all_data = range(len(fetch_data))

    # Extract the most popular keywords
    query = f"SELECT SUBSTRING_INDEX(SUBSTRING_INDEX({target_column}, ',', n), ',', -1) AS tag_word, COUNT(*) AS cnt FROM {main_table} CROSS JOIN (SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10) AS nums WHERE n <= 1 + LENGTH({target_column}) - LENGTH(REPLACE({target_column}, ',', '')) GROUP BY tag_word ORDER BY cnt DESC LIMIT 6;"
    cursor.execute(query)

    # Quick replies labels
    quick_replies_labels = [result[0] for result in cursor.fetchall()]

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

# Fallback message format
fallback_res = {
    "version": "2.0",
    "template": {
        "outputs": [{"simpleText": {"text": "데이터가 없습니다."}}],
        "quickReplies": quick_replies,
    },
}


# Function: Get category name from the request
async def get_category_name(req: dict) -> str:
    return req.get("action", {}).get("clientExtra", {}).get("name", "Read_Error!!!")


# Function: Send image response with data
async def send_img_res(
    items: list, block_id: str, category_name: str = "무작위"
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
                                "extra": {"name": category_name},
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


# Function: url check
async def url_check(check_data: list) -> list:
    items = []

    for result in check_data:
        if len(items) == 3:
            return items

        # Send a HTTP request to the image URL
        try:
            response = requests.get(result[1])
        except Exception as e:
            print("Response_passed", e)
            continue

        # Check status code and delete the failed URL
        if response.status_code != 200:
            # cursor.execute(
            #     f"DELETE FROM {main_table} WHERE url = '{result[1]}'")
            # conn.commit()

            # cursor.execute(
            #     f"INSERT IGNORE INTO {del_table} (img_id, url, text, hashtag, crawled_at, text_tag) VALUES (%s,%s,%s,%s,%s,%s)",
            #     result,
            # )
            # conn.commit()
            print("passed")
            pass

        else:
            # Add the URL to the list of items
            items.append(
                {
                    "thumbnail": {
                        "imageUrl": result[1],
                        "fixedRatio": True,
                        "link": {"web": result[1]},
                    },
                    "buttons": [
                        {"action": "share", "label": "공유하기", "messageText": "공유하기"}
                    ],
                }
            )

    return items


# Function: Get the image data from MySQL database
async def get_image_data(category_name: str = "무작위", custom_query="None"):
    # Images to be sent to Kakao

    # Connect to MySQL
    with mysql.connector.connect(**config) as conn:
        cursor = conn.cursor()

        # ﻿URL 컬럼 변경 : ﻿URL -> url
        # cursor.execute("ALTER TABLE tmp_data CHANGE ﻿URL url TEXT;")

        # Ad-hoc search algorithm
        if category_name == "무작위":
            random_list = random.sample(range_all_data, k=len(range_all_data))
            items = []
            for i in random_list:
                if len(items) == 3:
                    return items
                query = f"select * from {main_table} where id in ('{i}')"
                cursor.execute(query)
                a = await url_check(check_data=cursor.fetchall())
                items.extend(a)
                
            

        elif category_name != "무작위":
            query = f"SELECT * FROM {main_table} where {target_column} like ('%{category_name}%') ORDER BY RAND();"

        elif custom_query != "None":
            query = custom_query

        # Get the URLs from the main table
        cursor.execute(query)

        items = await url_check(check_data=cursor.fetchall())
        # Process each row of the result set

    return items


# Function: Get keyword from gpt
async def get_keyword_with_gpt(input_sentence: str) -> list:
    # Set up an API key to access the OpenAI API
    openai.api_key = os.getenv("api_key")

    # Extract key words from sentences using the GPT-3 model
    messages = [
        {"role": "user", "content": f"아래 문장에서 핵심단어를 3개만 추출해주세요. \n\n {input_sentence}"}
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages, temperature=0.2
    )
    category_name = completion.choices[0].message.content

    # Convert the extracted words into a list
    category_lists = category_name.split(", ")
    category_list = [category.rstrip(".") for category in category_lists]

    return category_list


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
                                    "imageUrl": "https://i.ibb.co/vkVxZGr/img-keyword.png"
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
                                    "imageUrl": "https://i.ibb.co/L6rmwns/img-sentence.png"
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
                                "title": "추천받을 감정 키워드를 선택해주세요.",
                                "thumbnail": {
                                    "imageUrl": "https://i.ibb.co/9hPWmDj/img-emotion.png"
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
                                "title": "추천받을 상황 키워드를 선택해주세요.",
                                "thumbnail": {
                                    "imageUrl": "https://i.ibb.co/TRR78L0/img-situation.png"
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
    req = await request.json()

    # Select category
    category_name = await get_category_name(req)

    items = await get_image_data(category_name)
    if len(items) == 0:
        return JSONResponse(content=fallback_res)

    return await send_img_res(items, block_id_send_img, category_name)


# Route: Send random images
@app.post("/send_img_random")
async def send_img_random(request: Request):

    items = await get_image_data()

    return await send_img_res(items, block_id_send_img_random)


# Route: Extract keyword and send images
@app.post("/talk_to_mememo")
async def talk_to_mememo(request: Request):
    req = await request.json()

    # Get the user input
    # word_limit : 32767 | 32767byte
    input_sentence = req["action"]["detailParams"]["contents"]["origin"]
    print(f"input_sentence : {input_sentence}")

    # Catching GPT-request limit errors
    try:
        answer = await get_keyword_with_gpt(input_sentence)
        print(f"answer : {answer}")
        # Get the number of elements in the answer list
        num_answers = len(answer)
    except Exception as e:
        print(e)
        return JSONResponse(content=fallback_res)

    # Construct a SQL query that looks for matches of each answer in the target column
    # by using the LIKE operator and concatenating multiple OR conditions.
    # For example: "text_tag LIKE '%0%' OR text_tag LIKE '%1%'"
    like_query = " OR ".join([f"{target_column} LIKE '%{a}%'" for a in answer])

    # Construct a SQL query that assigns a value of 1 to the count column for each match
    # and a value of 0 for each non-match using a CASE statement.
    # For example: "(CASE WHEN text_tag LIKE '%0%' THEN 1 ELSE 0 END) +
    #               (CASE WHEN text_tag LIKE '%1%' THEN 1 ELSE 0 END)"
    select_query = " + ".join(
        [f"(CASE WHEN {target_column} LIKE '%{a}%' THEN 1 ELSE 0 END)" for a in answer]
    )

    # Construct the final SQL query that selects all rows from the main table that have at least one match
    # to any element in the answer list, and calculates the count of matches for each row using the select_query.
    # The rows are ordered by the count of matches in descending order.
    if num_answers > 0:
        query = f"""
        SELECT *,
            ({select_query}) AS {count_column}
        FROM {main_table}
        WHERE {like_query}
        HAVING {count_column} >= 1
        ORDER BY {count_column} DESC;
        """
    print(query)
    items = await get_image_data(custom_query=query)

    if len(items) == 0:
        return JSONResponse(content=fallback_res)

    category_name = ""
    for i in answer:
        category_name += i

    return await send_img_res(items, block_id_send_img, category_name=category_name)


# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
