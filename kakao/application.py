from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import urllib
import requests
import mysql.connector

ERROR_MESSAGE = '네트워크 접속에 문제가 발생하였습니다. 잠시 후 다시 시도해주세요.'


app = Flask(__name__)

# MySQL connection configuration
config = {
    'host': 'localhost',
    'user': 'username',
    'password': '1234',
    'database': 'mysql'
}


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/weather', methods=['POST'])
def weather():

    req = request.get_json()

    location = req["action"]["detailParams"]["sys_location"]["value"]

    enc_loc = urllib.parse.quote(location + '+ 날씨')
    el = str(enc_loc)
    url = 'https://search.naver.com/search.naver'
    url = url + '?sm=top_hty&fbm=1&ie=utf8&query='
    url = url + el

    html = requests.get(url).text

    soup = BeautifulSoup(html, "lxml")

    tmp = soup.find_all("div", {"class": "_tab_flicking"})[0]
    tmp = tmp.find_all("div", {"class": "_today"})[0]
    tmp = tmp.find_all("div", {"class": "temperature_text"})[0]
    tmp = tmp.find_all("strong")[0]
    r3 = str(tmp.text).split("현재 온도")[-1].split('.')[0]

    answer = location + "의 온도는 " + r3 + "도 입니다."

    # 답변 텍스트 설정
    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ]
        }
    }

    # Connect to MySQL
    conn = mysql.connector.connect(**config)

    # Execute SQL query
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user limit 1')

    # Fetch results
    results = cursor.fetchall()

    # Close MySQL connection
    cursor.close()
    conn.close()
    print(results)

    return jsonify(res)


# 메인 함수
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
    # app.run(host='127.0.0.1', port=5000, threaded=True, debug = True)
