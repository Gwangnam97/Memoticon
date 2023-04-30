import uvicorn
import mysql.connector
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import requests


# 추후 신고 버튼 기능 ㄱ
# 키워드 추천에서 res에 담기는 키워드 추출 다시하기

# GPT - Error
# Rate limit reached for default-gpt-3.5-turbo in organization org-UXzHELPVXIX3JfmdJNpgWGBR on requests per min. Limit: 3 / min. Please try again in 20s. Contac
# t support@openai.com if you continue to have issues. Please add a payment method to your account to increase your rate limit. Visit https://platform.openai.co
# m/account/billing to add a payment method.


# Message form to send when there is no image data
tmp_res = {
    "version": "2.0",
    "template": {"outputs": [{"simpleText": {"text": "데이터가 없습니다."}}]},
}

# MySQL connection configuration
config = {"host": "localhost", "user": "root",
          "password": "1234", "database": "sys"}

app = FastAPI()

block_id_send_img_random = "644a0944b5e5636c2125a14c"
block_id_send_img = "64477498d853bb56940a87bd"

quick_replies_labels = ["기쁨", "슬픔", "분노", "황당", "놀람", "졸림"]
quick_replies = [
    {
        "label": label,
        "action": "block",
        "blockId": block_id_send_img,
        "extra": {"name": label},
    }
    for label in quick_replies_labels
]


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


async def get_category_name(req: dict):
    try:
        return req["action"]["clientExtra"]["name"]
    except KeyError:
        return "Read_Error!!!"


async def get_image_data(category_name: str = "None", random: bool = False):

    main_table = "sys.tmp_data"

    # Deleye & save rows to tmp.pinterest
    del_table = "tmp.pinterest"

    # Need to add search algorithm
    # ad-hoc search algorithm
    if random == False:
        query = f"SELECT ﻿URL FROM {main_table} where text_tag like ('%{category_name}%') ORDER BY RAND() LIMIT 3;"
    else:
        query = f"SELECT ﻿URL FROM {main_table} ORDER BY RAND() LIMIT 3;"

    # Images to be sent to Kakao
    items = []

    # Connect MySQL
    with mysql.connector.connect(**config) as conn:
        cursor = conn.cursor()

        # Get the URLs from the main table
        cursor.execute(query)
        results = cursor.fetchall()

        # Check the HTTP status code for each URL
        for result in results:
            response = requests.get(result[0])

            # Separate deleted image url
            if response.status_code != 200:
                # Delete the URL from the main table
                delete_query = f"DELETE FROM {main_table} WHERE url = '{result[0]}'"
                cursor.execute(delete_query)
                conn.commit()

                # Save the URL to the temporary table
                insert_query = f"INSERT INTO {del_table} (url) VALUES ('{result[0]}')"
                cursor.execute(insert_query)
                conn.commit()

                # Skip to the next URL
                continue

            # Add the URL to the list of items
            items.append({
                "imageUrl": result[0],
                "link": {"web": result[0]},
            })

    return items


@app.post("/send_img")
async def send_img(request: Request):
    req = await request.json()

    # select category
    category_name = await get_category_name(req)

    items = await get_image_data(category_name)

    if len(items) == 0:
        return JSONResponse(content=tmp_res)

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
                                "blockId": block_id_send_img,
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


@app.post("/send_img_random")
async def send_img_random(request: Request):
    req = await request.json()
    print(req)

    # select category
    # category_name = await get_category_name(req)
    category_name = ""

    items = await get_image_data(category_name, random=True)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "무작위의 밈을 추천해드립니다. "
                        "더 많은 밈을 보고싶은 경우 아래의 더보기를 눌러주세요",
                        "buttons": [
                            {
                                "action": "block",
                                "label": "더보기",
                                "blockId": block_id_send_img_random,
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


@app.post("/talk_to_mememo")
async def talk_to_mememo(request: Request):
    req = await request.json()

    try:
        # 입력받는 문장
        input_content = req["action"]["detailParams"]["contents"]["origin"]

        import openai

        # 키 값 백업해야할듯
        openai.api_key = "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"

        messages = []
        question = input_content

        messages.append(
            {
                "role": "user",
                "content": f"Please extract only one key word in Korean from the sentence below \n\n {question}",
            }
        )

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        category_name = completion["choices"][0]["message"]["content"]

        items = await get_image_data(category_name)

        if len(items) == 0:
            return JSONResponse(content=tmp_res)

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
                                    "blockId": block_id_send_img,
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
    except Exception as e:
        print(e)
        res = tmp_res

    return JSONResponse(content=res)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
