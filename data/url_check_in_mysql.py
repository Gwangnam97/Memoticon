import aiomysql
import asyncio
import aiohttp

block_id_send_img_random = "644a0944b5e5636c2125a14c"
block_id_send_img = "64477498d853bb56940a87bd"


config = {
    "host": "52.78.88.87",
    "port": 54978,
    "user": "root",
    "password": "1234",
    "db": "sys"
}


main_table = "sys.main"
del_table = "sys.del_history"
count_column = "count_sum"
target_column = "hashtag"


async def create_pool():
    print("creating pool")
    global pool
    pool = await aiomysql.create_pool(**config)


async def init_cache():
    print("start init_cache")
    global cache_data
    global range_all_data
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:

            await cur.execute("SELECT * FROM main;")

            cache_data = await cache_url_check(await cur.fetchall(), conn, cur)
            print(f'len(cache_data) : {len(cache_data)}')
            range_all_data = range(len(cache_data))
            print(f'done init_cache')


async def cache_url_check(cache_data: list, conn, cur) -> list:
    print("start cache_url_check")
    valid_urls = []

    timeout = aiohttp.ClientTimeout(total=None)
    async with aiohttp.ClientSession(timeout=timeout) as session:

        tasks = []
        print("start process_url")
        for cache_url in cache_data:
            tasks.append(await process_url(
                session, cache_url, cur, conn, valid_urls))

        await asyncio.gather(*tasks)
    print(f'len(tasks) : {len(tasks)}')
    print(f'len(valid_urls) : {len(valid_urls)}')
    return valid_urls


async def process_url(session, cache_url, cur, conn, valid_urls):
    try:
        async with session.get(cache_url[1]) as response:
            if response.status != 200:
                print("Response.status != 200 !!!")
                print(f"id : {cache_url[0]}")
                print(f"url : {cache_url[1]}")
                print(f"hashtag : {cache_url[2]}")

                await cur.execute(f"DELETE FROM {main_table} WHERE url = '{cache_url[1]}'")
                await cur.execute(f"INSERT IGNORE INTO {del_table} (img_id, url, hashtag) VALUES (%s,%s,%s)", (cache_url[0], cache_url[1], cache_url[2]))

                await conn.commit()
            else:
                print(f"id : {cache_url[0]}")
                valid_urls.append(cache_url)

    except aiohttp.ClientError:
        pass

    return valid_urls


async def on_startup():  # Register an event handler to create a database connection pool when the app starts up
    print("SEVER startup")
    await create_pool()
    # Register the update_cache_every_hour coroutine with the asyncio event loop
    await init_cache()

asyncio.run(on_startup())
