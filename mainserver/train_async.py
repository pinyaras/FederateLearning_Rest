import concurrent.futures
import urllib.request
# from urllib import HTTPError
from fl_agg import model_aggregation
from main_server import send_agg_to_client
import requests, json
from datetime import datetime
# URLS = ['http://www.foxnews.com/',
#         'http://www.cnn.com/',
#         'http://europe.wsj.com/',
#         'http://www.bbc.co.uk/',
#         'http://some-made-up-domain.com/']

URLS = ['http://localhost:8001/modeltrain', 'http://localhost:8002/modeltrain']
clients = ['http://localhost:8001/', 'http://localhost:8002/']

def fetch(url):
    try:
        url += 'modeltrain'
        response = requests.get(url)
        # print(datetime.now().strftime('%H:%M:%S'))
        # print(url)
        return response.text()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    else:
        print('Success!')

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    print("start training")
    print(datetime.now().strftime('%H:%M:%S'))
    future_to_url = {executor.submit(fetch, url): url for url in clients}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            print("Done training")
            print(url)
            print(datetime.now().strftime('%H:%M:%S'))
            model_aggregation()
            send_agg_to_client(url)

        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))