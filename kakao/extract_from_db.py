# %%
import MySQLdb
from MySQLdb.cursors import DictCursor
import random
# DictCursor는 기본 커서보다 더 많은 메모리를 사용하므로, cursorclass 매개변수를 사용하여 기본 커서로 변경함

# Connect to MySQL
conn = MySQLdb.connect( 
    host="localhost",
    user="root",
    passwd="1234",
    db="crawl_data",
    charset='utf8',
    cursorclass=DictCursor,
)

if __name__=="__main__":
    try:
        with conn.cursor() as cursor:
            # Execute the SQL query
            hashtag = "mbti"
            table = 'crawl_test'
            sql = f'SELECT url FROM {table} WHERE hashtags LIKE %s'
            # cursor.execute(sql, ('%' + hashtag + '%',))
            cursor.execute('SELECT * FROM crawl_test limit 1')
            # Fetch and print the results
            results = cursor.fetchall()
            print(f'len(results): {len(results)}')

            # Print 3 random rows
            random_rows = random.sample(results, k=min(3, len(results)))

            url_list = []
            for row in random_rows:
                # print(row['url'])
                url_list.append(row['url'])
            print(url_list)
            
    finally:
        # Close the MySQL connection
        conn.close()
