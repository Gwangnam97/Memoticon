# drop face_book

from facebook_scraper import get_posts
import MySQLdb  # pipenv install mysqlclient
import time
from MySQLdb.cursors import DictCursor
# import warnings
# # Disable warnings
# warnings.filterwarnings('ignore')

# List of columns to store in the database
column_list = ['post_id', 'text', 'post_text', 'shared_text', 'original_text', 'time', 'timestamp', 'image', 'image_lowquality', 'images', 'images_description', 'images_lowquality', 'images_lowquality_description', 'video', 'video_duration_seconds', 'video_height', 'video_id', 'video_quality', 'video_size_MB', 'video_thumbnail', 'video_watches', 'video_width',
               'likes', 'comments', 'shares', 'post_url', 'link', 'links', 'user_id', 'username', 'user_url', 'is_live', 'factcheck', 'shared_post_id', 'shared_time', 'shared_user_id', 'shared_username', 'shared_post_url', 'available', 'comments_full', 'reactors', 'w3_fb_url', 'reactions', 'reaction_count', 'with', 'page_id', 'sharers', 'image_id', 'image_ids', 'was_live']

# Format column names for the database
target_col = ', '.join((f"F_{i}" for i in column_list))
formatting_col = ','.join(["%s"] * len(column_list))

# List of search queries
# query_list = ["nintendo", "LJYTOON", "funny"]
query_list = ["nintendo", "LJYTOON", "이주용"]

# List of keywords to filter out
filter_list = ['19금', 'sexy', 'ass', '섹시']

# Database table name
table_name = "facebook_crawler"

# Connect to the MySQL database
conn = MySQLdb.connect(
    user="root",
    passwd="1111",
    host="localhost",
    cursorclass=DictCursor,
    db="crawl_data",
    charset='utf8mb4',
    use_unicode=True
)

# Create a cursor object
cursor = conn.cursor()

# Set character encoding for MySQL connection and query string
cursor.execute("set character_set_connection=utf8;")
cursor.execute("set character_set_server=utf8;")
cursor.execute("set character_set_client=utf8;")
cursor.execute("set character_set_results=utf8;")
cursor.execute("set character_set_database=utf8;")

# Drop and recreate the table
cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
cursor.execute(
    f"CREATE TABLE {table_name} (id INT PRIMARY KEY AUTO_INCREMENT)")

for column in column_list:
    cursor.execute(
        f"ALTER TABLE {table_name} ADD COLUMN F_{column} TEXT NOT NULL")
    conn.commit()

# Start crawling
start_time = time.time()


def crawl_facebook(crawl_query, pages=3):
    print(crawl_query)

    for i, post in enumerate(get_posts(crawl_query, pages=pages)):
        # Stop crawling after reaching the specified number of pages
        if i == pages:
            break

        # Skip posts containing filtered keywords
        for item in filter_list:
            if item in post['post_text']:
                break

        else:
            # Insert post data into the database
            values = [str(post.get(col, '')).encode('utf-8')
                      for col in column_list]
            query = f"INSERT IGNORE INTO {table_name} ({target_col}) VALUES ({formatting_col})"

            try:
                cursor.execute(query, values)
            except Exception as e:
                print(e)
                continue

            conn.commit()


for i in query_list:
    crawl_facebook(i, pages=3)


# Close the database connection
cursor.close()
conn.close()

# Print the execution time
print("=" * 80)
print("Execution time:", time.time() - start_time)
print("Done")
