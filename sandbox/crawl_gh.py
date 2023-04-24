# %%
import time
import snscrape.modules.twitter as sntwitter
import MySQLdb
from MySQLdb.cursors import DictCursor

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
    limit = 500   # limit = 50000 으로 수정해야 100만개 이상 뽑힐듯

    # 검색(crawl) 할 리스트
    crawl_query_list = ["#밈", "#짤방", "#유머",]

    # 검색도중 필터링 할 리스트
    filtering_list = ['19금', '섹시', 'sexy', 'ass', '테스트']

    def crawl_commit_to_sql(tweet_search_query):

        # Using TwitterSearchScraper to scrape data and append tweets to list
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(tweet_search_query).get_items()):
            if i == limit:
                print("="*180, f"\n{tweet_search_query} Done!!")
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
                #   tweet.content, tweet.hashtags, tweet.media]
            # column_list = ['date', 'user_id', 'content', 'hashtags', 'media']

            # 멘토 曰 : 필요한 내용은 url , 본문 , 해시태그 정도
            query = 'INSERT IGNORE INTO crawl_test (date, url, user_id, content, hashtags, media) VALUES (%s,%s,%s,%s,%s,%s)'
            values = (tweet.date, str(tweet.url).encode('utf-8'), str(tweet.id).encode('utf-8'), str(tweet.content).encode(
                'utf-8'), str(tweet.hashtags).encode('utf-8'), str(tweet.media).encode('utf-8'))

            try:
                cursor.execute(query, values)

            # Error_Catch
            except Exception as e:
                print("="*180, e, tweet.content, "="*180)
                pass

            conn.commit()

    for i in crawl_query_list:
        crawl_commit_to_sql(i)

    cursor.close()
    conn.close()

print("="*180, "\ntime :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간
