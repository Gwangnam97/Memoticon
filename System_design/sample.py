from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.programming.framework import FastAPI
from diagrams.programming.flowchart import Database
from diagrams.custom import Custom
from urllib.request import urlretrieve


path = "C:/Memoticon/System_design/"

with Diagram(
    "Python Code Diagram",
    show=False,
    filename=path + "python_code_diagram.png",
    direction="LR",
):
    with Cluster("user"):
        urlretrieve("https://i.ibb.co/Bzb6KNd/pngwing-com.png", path + "user.png")
        user = Custom("user", path + "user.png")

    with Cluster("kakao"):
        urlretrieve("https://i.ibb.co/BKXJzKr/Yellow.png", path + "kakao.png")
        kakao = Custom("kakao", path + "kakao.png")

    with Cluster("Code"):
        tracemalloc = Python("tracemalloc")
        openai = Python("openai")
        uvicorn = Python("uvicorn")
        aiohttp = Python("aiohttp")
        asyncio = Python("asyncio")
        aiomysql = Python("aiomysql")

    with Cluster("Framework"):
        fastapi = FastAPI("FastAPI")

    with Cluster("Dependency"):
        jsonresponse = Python("JSONResponse")
        request = Python("Request")

    with Cluster("Database"):
        database = Database("FastAPI")

    # started = user
    start = kakao
    end = database

    # started >> start

    start >> tracemalloc
    start >> openai
    start >> uvicorn
    start >> aiohttp
    start >> asyncio
    start >> aiomysql

    tracemalloc >> jsonresponse
    openai >> request
    uvicorn >> jsonresponse
    aiohttp >> request
    asyncio >> jsonresponse
    aiomysql >> request

    jsonresponse >> fastapi
    request >> fastapi

    fastapi >> end
