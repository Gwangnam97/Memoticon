import uvicorn
import mysql.connector
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request


# 컨텍스트 생성하기 (기쁨->슬픔)
# 퀵 리플 만들기

# MySQL connection configuration
config = {"host": "localhost", "user": "root", "password": "1234", "database": "sys"}

app = FastAPI()


@app.post("/recommend")
async def recommend(request: Request):
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": "✨추천 도와드릴게요!\n☝우선 어떻게 추천해줄지 정해볼까요?"}},
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
        return "None"


async def get_image_data(category_name: str):
    # query = f"SELECT url FROM sys.pinterest where crawled_at like ('%{category_name}%') ORDER BY RAND() LIMIT 3;"
    query = "SELECT url FROM sys.pinterest where crawled_at like ('%짤방%') ORDER BY RAND() LIMIT 3;"

    with mysql.connector.connect(**config) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()

    items = [
        {
            "title": f"listCard 테스트#{index + 1}",
            "description": f"listCard 테스트#{index + 1} description",
            "imageUrl": result[0],
            "link": {"web": result[0]},
        }
        for index, result in enumerate(results)
    ]

    return items


@app.post("/send_img")
async def send_img(request: Request):
    req = await request.json()
    category_name = await get_category_name(req)
    block_id = "64415440013416338a0853a3"
    items = await get_image_data(category_name)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": f"{category_name}에 맞는 밈을 추천해드립니다. "
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
                    "listCard": {
                        "header": {"title": "listCard 테스트"},
                        "items": items,
                    }
                },
            ]
        },
    }

    return JSONResponse(content=res)


@app.post("/send_img_random")
async def send_img_random(request: Request):
    req = await request.json()
    block_id = "64415440013416338a0853a3"
    category_name = "tmp"
    items = await get_image_data(category_name)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": "무작위의 밈을 추천해드립니다. " "더 많은 밈을 보고싶은 경우 아래의 더보기를 눌러주세요",
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
                    "listCard": {
                        "header": {"title": "listCard 테스트"},
                        "items": items,
                    }
                },
            ]
        },
    }

    return JSONResponse(content=res)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
