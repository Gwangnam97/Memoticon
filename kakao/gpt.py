import random
import re
import mysql.connector
from kakao_work_sdk.auth import KakaoWorkAuth
from kakao_work_sdk.message import Message
from kakao_work_sdk.conversation import Conversation

# 카카오 워크 API 토큰
token = "your_kakao_work_api_token"

# MySQL 접속 정보
mysql_config = {
    'host': 'your_mysql_host',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'your_mysql_database'
}

# 인증
auth = KakaoWorkAuth(token)

# 대화방 조회
conv_api = Conversation(auth)
conv_list = conv_api.get_conversations()
for conv in conv_list:
    print(conv['id'], conv['name'])

# 해시태그 추출 함수
def extract_hashtags(text):
    return re.findall(r'\#\w+', text)

# 이미지 URL 가져오기
def get_image_urls(hashtags):
    cnx = mysql.connector.connect(**mysql_config)
    cursor = cnx.cursor()
    query = "SELECT img FROM crawl_data WHERE "
    for tag in hashtags:
        query += f"text LIKE '%{tag}%' AND "
    query = query[:-5]  # 마지막 AND 제거
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    urls = [result[0] for result in results if result[0] is not None]
    return urls

# 메시지 보내기
def send_image_messages(images, conversation_id):
    msg_api = Message(auth)
    for i in range(3):
        if not images:  # 이미지가 없으면 중단
            break
        img_url = random.choice(images)
        msg = f"[{i+1}] {img_url}"
        msg_api.send_message(msg, conversation_id=conversation_id)
        images.remove(img_url)

# 메시지 처리 함수
def process_message(text, conversation_id):
    hashtags = extract_hashtags(text)
    images = get_image_urls(hashtags)
    send_image_messages(images, conversation_id)

# 봇 실행
while True:
    events = conv_api.get_events()
    for event in events:
        if event['type'] == 'message' and event['conversation_id'] is not None:
            text = event['text']
            conversation_id = event['conversation_id']
            process_message(text, conversation_id)
