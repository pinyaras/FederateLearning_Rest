import ast
import math
import time
import requests, json
import concurrent.futures
import asyncio, aiohttp

from fl_agg import model_aggregation
from main_server import send_agg_to_clients

from requests.exceptions import HTTPError
from datetime import datetime 


URLS = ['http://localhost:8001/modeltrain', 'http://localhost:8002/modeltrain']

def sequencetial():
    for url in ['http://localhost:8001/modeltrain', 'http://localhost:8002/modeltrain']:
        try:
            response = requests.get(url)

            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Success!')


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

async def sync():
    urls = ['http://localhost:8001/modeltrain', 'http://localhost:8002/modeltrain']
    tasks = []

    async with aiohttp.ClientSession() as session:
        for url in URLS:
            tasks.append(fetch(session, url))
        results = await asyncio.gather(*tasks)
    model_aggregation()
    send_agg_to_clients()
    # response = requests.get('http://localhost:8002/send_model_clients')

async def main_sync():
    for i in range(1,10):
        print("Epoch", i)

        await sync()


loop = asyncio.get_event_loop()
loop.run_until_complete(main_sync())

# start_time = time.time()
# for i in range(1):
#     print("Epoch", i)
#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(main())
#     await main()
#     elapsed_time = time.time() - start_time
#     time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

#     model_aggregation()
#     send_agg_to_clients()
#     response = requests.get('http://localhost:8002/send_model_clients')
#     start_time = time.time()

