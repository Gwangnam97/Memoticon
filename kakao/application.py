import uvicorn
import mysql.connector
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import requests
import openai

app = FastAPI()

# Define blocks ID
block_id_send_img_random = "644a0944b5e5636c2125a14c"
block_id_send_img = "64477498d853bb56940a87bd"


# MySQL connection configuration
config = {"host": "localhost", "user": "root", "password": "1234", "database": "sys"}

# Define tables, Delete & save rows to del_history
main_table = "sys.tmp_data"
del_table = "del_history"

# Connect to MySQL
with mysql.connector.connect(**config) as conn:
    cursor = conn.cursor()

    target_column = "text_tag"
    query = f"SELECT SUBSTRING_INDEX(SUBSTRING_INDEX({target_column}, ',', n), ',', -1) AS tag_word, COUNT(*) AS cnt FROM {main_table} CROSS JOIN (SELECT 1 AS n UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9 UNION ALL SELECT 10) AS nums WHERE n <= 1 + LENGTH({target_column}) - LENGTH(REPLACE({target_column}, ',', '')) GROUP BY tag_word ORDER BY cnt DESC LIMIT 6;"

    # Get the URLs from the main table
    cursor.execute(query)

    # Quick replies labels
    quick_replies_labels = []
    # Process each row of the result set
    for result in cursor.fetchall():
        quick_replies_labels.append(result[0])

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


# Function: Get the image data from MySQL database
async def get_image_data(category_name: str = "None", random: bool = False):
    # Images to be sent to Kakao
    items = []

    # Connect to MySQL
    with mysql.connector.connect(**config) as conn:
        cursor = conn.cursor()

        # ﻿URL 컬럼 변경 : ﻿URL -> url
        # cursor.execute("ALTER TABLE tmp_data CHANGE ﻿URL url TEXT;")

        # Ad-hoc search algorithm
        if random == False:
            query = f"SELECT * FROM {main_table} where text_tag like ('%{category_name}%') ORDER BY RAND() LIMIT 90;"
        else:
            query = f"SELECT * FROM {main_table} ORDER BY RAND() LIMIT 90;"

        # Get the URLs from the main table
        cursor.execute(query)

        # Process each row of the result set
        for result in cursor.fetchall():
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
                cursor.execute(f"DELETE FROM {main_table} WHERE url = '{result[1]}'")
                conn.commit()

                cursor.execute(
                    f"INSERT IGNORE INTO {del_table} (img_id, url, text, hashtag, crawled_at, text_tag) VALUES (%s,%s,%s,%s,%s,%s)",
                    result,
                )
                conn.commit()

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
    items = await get_image_data(random=True)

    return await send_img_res(items, block_id_send_img_random)


# Route: Extract keyword and send images
@app.post("/talk_to_mememo")
async def talk_to_mememo(request: Request):
    req = await request.json()

    # Get the user input , word_limit : 32767 | 32767byte
    question = req["action"]["detailParams"]["contents"]["origin"]

    # Set OpenAI API Key
    openai.api_key = "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"

    messages = [
        {
            "role": "user",
            "content": f"아래 문장에서 핵심단어 하나만 추출해주세요. \n\n {question}",
        }
    ]

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

        # GPT's response
        category_name = completion["choices"][0]["message"]["content"]

        items = await get_image_data(category_name=category_name, random=False)

    except Exception as e:
        print(e)
        return JSONResponse(content=fallback_res)

    if len(items) == 0:
        return JSONResponse(content=fallback_res)

    return await send_img_res(items, block_id_send_img, category_name)


# Run the FastAPI application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
