import mysql.connector


async def get_image_data(category_name: str):
    # query = f"SELECT url FROM sys.pinterest where crawled_at like ('%{category_name}%') ORDER BY RAND() LIMIT 3;"
    query = "SELECT url FROM sys.pinterest where crawled_at like ('%짤방%') ORDER BY RAND() LIMIT 3;"

    # Deleye & save rows to tmp.pinterest
    tmp_table = "tmp.pinterest"

    items = []

    with mysql.connector.connect(**config) as conn:
        cursor = conn.cursor()

        # Get the URLs from the main table
        cursor.execute(query)
        results = cursor.fetchall()

        # Check the HTTP status code for each URL
        for result in results:
            response = requests.get(result[0])
            if response.status_code != 200:
                # Delete the URL from the main table
                delete_query = f"DELETE FROM sys.pinterest WHERE url = '{result[0]}'"
                cursor.execute(delete_query)
                conn.commit()

                # Save the URL to the temporary table
                insert_query = f"INSERT INTO {tmp_table} (url) VALUES ('{result[0]}')"
                cursor.execute(insert_query)
                conn.commit()

                # Skip to the next URL
                continue

            # Add the URL to the list of items
            items.append({
                "imageUrl": result[0],
                "link": {"web": result[0]},
            })

    return items
