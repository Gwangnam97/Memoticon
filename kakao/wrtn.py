# pip install pymysql
# pip install flask
# pip install requests


import pymysql
import random
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def get_images_by_hashtag(hashtag):
    db = pymysql.connect(host="your_mysql_host", user="your_mysql_user", password="your_mysql_password", database="your_mysql_database")
    cursor = db.cursor()
    sql = "SELECT img FROM crawl_data WHERE text LIKE %s LIMIT 3"
    cursor.execute(sql, ('%#' + hashtag + '%',))
    images = [row[0] for row in cursor.fetchall()]
    db.close()
    return images

def send_image(url, user_id):
    kakao_api_url = "https://your_kakao_api_url"
    headers = {
        "Authorization": "your_api_key",
        "Content-Type": "application/json"
    }
    data = {
        "receiver_uuids": [user_id],
        "template_id": "your_image_template_id",
        "template_args": {
            "imageUrl": url
        }
    }
    requests.post(kakao_api_url, headers=headers, json=data)

@app.route('/kakao-bot', methods=['POST'])
def kakao_bot():
    data = request.get_json()
    user_id = data['user_id']
    message = data['message']

    hashtag = message.replace("#", "").strip()
    images = get_images_by_hashtag(hashtag)
    random.shuffle(images)

    for img in images:
        send_image(img, user_id)

    response = {"message": "이미지를 전송했습니다!"}
    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)