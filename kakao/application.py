import uvicorn
import mysql.connector
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
import time

# MySQL connection configuration
config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'sys'
}

app = FastAPI()


@app.post('/weather')
async def weather(request: Request):
    
    # Start crawling
    start_time = time.time()
    req = await request.json()
    # location = req["action"]["detailParams"]["sys_location"]["value"]

    # Connect to MySQL
    conn = mysql.connector.connect(**config)

    # Execute SQL query
    cursor = conn.cursor()
    cursor.execute('SELECT url FROM teeest ORDER BY RAND() LIMIT 3')

    # Fetch results
    results = cursor.fetchall()

    # Format response
    items = []
    for result in results:
        item = {
            "title": f"listCard 테스트#{results.index(result) + 1}",
            "description": f"listCard 테스트#{results.index(result) + 1} description",
            "imageUrl": result[0],
            "link": {"web": result[0]}
        }
        items.append(item)

    res = {"version": "2.0",
           "template": {"outputs": [{
               "listCard": {
                   "header": {"title": "listCard 테스트"},
                   "items": items,
                   "buttons": [{
                       "label": "네이버링크",
                       "action": "webLink",
                       "webLinkUrl": "https://www.naver.com"
                   }]
               }
           }]
           }
           }

    cursor.close()
    conn.close()
    print("Execution time:", time.time() - start_time)
    return JSONResponse(content=res)


if __name__ == 'main':
    uvicorn.run(app, host='0.0.0.0', port=5000)
