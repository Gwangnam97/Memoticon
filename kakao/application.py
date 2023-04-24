import uvicorn
import mysql.connector
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import time

# MySQL connection configuration
config = {"host": "localhost", "user": "root", "password": "1234", "database": "sys"}

app = FastAPI()


@app.post("/recommend")  # 추천해주기
async def recommend(request: Request):
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": "추천 도와드릴게요!\n우선  어떻게 추천해줄지 정해볼까요?"}},
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


@app.post("/send_img_random")  # 사진 랜덤으로 3개 보내기
async def send_img_random(request: Request):
    req = await request.json()

    try:
        category_name = req["action"]["clientExtra"]["name"]
    except:
        category_name = "None"
    block_id = "64415440013416338a0853a3"

    # Connect to MySQL
    conn = mysql.connector.connect(**config)

    # Execute SQL query
    cursor = conn.cursor()
    cursor.execute(
        "SELECT url FROM sys.pinterest where crawled_at like ('%짤방%') ORDER BY RAND() LIMIT 3;"
    )

    # Fetch results
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    # Format response
    items = []
    for result in results:
        item = {
            "title": f"listCard 테스트#{results.index(result) + 1}",
            "description": f"listCard 테스트#{results.index(result) + 1} description",
            "imageUrl": result[0],
            "link": {"web": result[0]},
        }
        items.append(item)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "basicCard": {
                        "title": category_name
                        + "에 맞는 밈을 추천해드립니다 더 많은 밈을 보고싶은 경우 아래의 더보기를 눌러주세요",
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
