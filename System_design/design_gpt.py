"""
시작은 사용자로부터 시작되고 사용자가 kakaotalk 메신저로 나의 chatbot에 메시지를 보내면 우선 메시지가 chatbot에 학습된 메시지일 때 kakaoapi에서 내가 만든 fastapi를 활용한 uvicorn 서버에서 생성한 MPA방식의 라우팅 페이지로 json 데이터를 전송하고 페이지에서 입력받은 데이터에서 keyword라는 키 값만 추출하여 서버가 켜질 때 mysql에서 cash변수에 테이블의 모든 값을 저장한 데이터에서 keyword 값이 포함된 img_url을 json데이터로 다시 kakaoapi로 전송하고 결국엔 kakaotalk메신저로 유저가 확인합니다."""

from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import Fastapi
from diagrams.onprem.database import Mysql
from diagrams.custom import Custom
from urllib.request import urlretrieve
from diagrams.k8s.controlplane import API
# from diagrams.gcp.api import APIGateway as API

# 구름 아이콘 diagrams.gcp.devtools.SDK


with Diagram("System Architecture", show=False, direction="TB"):
    with Cluster("User"):
        user = User("User")

    with Cluster("KakaoTalk"):
        urlretrieve("https://i.ibb.co/BKXJzKr/Yellow.png", "KakaoTalk.png")
        kakao_talk = Custom("KakaoTalk", "KakaoTalk.png")

    with Cluster("GoormIDE"):
        # uvicorn = Uvicorn("Uvicorn")
        urlretrieve(
            "https://raw.githubusercontent.com/tomchristie/uvicorn/master/docs/uvicorn.png", "Uvicorn.png")
        uvicorn = Custom("Uvicorn", "Uvicorn.png")
        fastapi = Fastapi("FastAPI")

    with Cluster("ChatGPT-API"):
        urlretrieve("https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/ChatGPT_logo.svg/120px-ChatGPT_logo.svg.png", "ChatGPT-API.png")
        chatgpt = Custom("ChatGPT", "ChatGPT-API.png")

    with Cluster("MySQL"):
        mysql = Mysql("MySQL")

    with Cluster("KakaoAPI"):
        kakao_api = API("KakaoAPI")

    user >> kakao_talk >> user

    kakao_talk >> kakao_api >> kakao_talk

    kakao_api >> fastapi >> kakao_api

    chatgpt >> fastapi >> chatgpt
    
    fastapi >> mysql >> fastapi
    # fastapi >> uvicorn >> fastapi
    fastapi - uvicorn


