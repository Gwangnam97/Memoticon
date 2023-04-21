import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Ajou notices server", description="for Kakao Chatbot", version="1.0.0"
)
app.add_middleware(  # 미들웨어 CORS
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/")
def hello():
    return "Welcome to my first_server, the server is running well."


# http링크/schedule로 스킬 서버를 연결
@app.post("/schedule")



    return JSONResponse()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
