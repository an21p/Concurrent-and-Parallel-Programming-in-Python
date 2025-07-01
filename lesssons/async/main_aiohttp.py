import asyncio
import time
import aiohttp
import requests


async def get_url_response(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
        
async def main():
    urls = ['https://google.com',
            'https://python.org',
            'https://finance.yahoo.com',
            'https://jmbld.fun']
    
    start = time.time()
    sync_text_response = []
    for url in urls:
        sync_text_response.append(requests.get(url).text) # NOTE: this is totally syncronous no awaits so even if we moved it to an await class it would not run faster (dows not give back control to the event loop, unlike the function above)

    end_time = time.time()

    print(f"sync: {end_time-start}")

    start = time.time()
    tasks = []
    for url in urls:
        tasks.append(asyncio.create_task(get_url_response(url)))

    async_text_response = await asyncio.gather(*tasks)

    end_time = time.time()

    print(f"async: {end_time-start}")


asyncio.run(main())
