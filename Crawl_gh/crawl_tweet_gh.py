# %%
import time
import snscrape.modules.twitter as sntwitter
import MySQLdb  # pipenv install mysqlclient
from MySQLdb.cursors import DictCursor


def crawl_commit_to_sql(tweet_search_query):

    # Using TwitterSearchScraper to scrape data and append tweets to list
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(tweet_search_query).get_items()):
        if i == limit:
            print("="*100, f"\n{tweet_search_query} Done!!")
            break

        found = 0

        for item in filtering_list:
            if item in tweet.content:
                found = 1
                break

        if found == 1:
            continue

        # a = emoji.demojize(str(tweet.content).split("http")[0])
        # IGNORE 중복 안되게? 검색 해봐야할듯
        # query_list = [tweet.date, tweet.id,
        #       tweet.content, tweet.hashtags, tweet.media]
        # column_list = ['date', 'user_id', 'content', 'hashtags', 'media']

        # 멘토 曰 : 필요한 내용은 url , 본문 , 해시태그 정도
        query = 'INSERT IGNORE INTO crawl_test (date, url, user_id, content, hashtags, media) VALUES (%s,%s,%s,%s,%s,%s)'
        values = (tweet.date, str(tweet.url).encode('utf-8'), str(tweet.id).encode('utf-8'), str(tweet.content).encode(
            'utf-8'), str(tweet.hashtags).encode('utf-8'), str(tweet.media).encode('utf-8'))

        try:
            cursor.execute(query, values)

        # Error_Catch
        except Exception as e:
            print("="*100, e, "="*100)
            pass

        conn.commit()

# Connect to MySQL
conn = MySQLdb.connect(
    user="root",
    passwd="1234",
    host="localhost",
    cursorclass=DictCursor,
    db="crawl_data",
    charset='utf8',
    use_unicode=True
)

# Create a cursor object
cursor = conn.cursor()

# Set character encoding for MySQL connection and query string
conn.query("set character_set_connection=utf8;")
conn.query("set character_set_server=utf8;")
conn.query("set character_set_client=utf8;")
conn.query("set character_set_results=utf8;")
conn.query("set character_set_database=utf8;")
# Drop and recreate the 'crawl' table
cursor.execute("DROP TABLE IF EXISTS crawl_test")
cursor.execute("""
    CREATE TABLE crawl_test (
        id INT PRIMARY KEY AUTO_INCREMENT,
        url TEXT NULL,
        date DATETIME NULL,
        user_id TEXT NULL,
        content TEXT NULL,
        hashtags TEXT NULL,
        media TEXT NULL
    )
""")

conn.commit()

if __name__ == "__main__":
    start = time.time()  # 시작 시간 저장

    # Define query and limit  (ex) example_query = "#밈 since:2020-04-01 until:2023-04-01" -> 4732개
    limit = 10000   # 크롤 횟수 limit = 50000 으로 수정해야 100만개 이상 뽑힐듯

    # 검색(crawl) 할 리스트
    crawl_query_list = ['#밈 고양이', '#밈', '#밈 짤', '#밈 강아지', '#밈 절망',
                        '#밈 한국어', '#밈 그리기', '#밈 유머 짤', '#짤 모음',
                        '#짤 말풍선', '#짤 귀여운', '#짤방', '#짤방 모음', '#짤방 대전을 시작하지',
                        '#짤방 gif', '#웃긴 짤방', '#29살 짤방', '#트위터 짤방', '#트위터',
                        '#고양이 짤방', '#무한도전 짤방', '#직장인 짤방', '#해리포터 짤방', '#mbti짤',
                        '#mbti밈', '#인터넷 밈 짤', '#동물 짤 밈', '#밈 짜증', '#짜증나는 밈',
                        '#웃긴 밈 짜증', '#짜장면 밈', '#짜파게티 밈', '#짜증날 때 밈', '#행복할 때 밈',
                        '#슬플 때 밈', '#유용한 짤', '#카톡할때 유용한 짤', '#유용한 카톡 짤', '#짤 저장소']
    crawl_query_list = [
        query + " since:2000-01-01 until:2023-04-16" for query in crawl_query_list]

    # 검색도중 필터링 할 리스트
    filtering_list = ['19금', '섹시', 'sexy', 'ass', '테스트']

    for i in crawl_query_list:
        crawl_commit_to_sql(i)

    cursor.close()
    conn.close()

print("="*180, "\ntime :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
