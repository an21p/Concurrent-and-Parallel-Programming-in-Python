import time
import random
import logging
from datetime import datetime, timezone
from multiprocessing import Queue
from queue import Empty
from typing import List

import yfinance as yf

@staticmethod
def get_next_symbol(queue: Queue, output: List[Queue]):
    if not isinstance(output, list):
        output = [output]
    
    while True:
        try:
            val = queue.get(timeout=20)
        except Empty:
            logging.warning('Queue timeout reached, stopping')
            break
        if val == 'DONE':
            for out in output:
                out.put('DONE')
            break
        price = get_yahoo_data(val)
        for out in output:
            out.put((val, price, datetime.now(timezone.utc)))
        logging.info(f"{val},{price}")
        time.sleep(20 * random.random())

@staticmethod
def get_yahoo_data(symbol: str):
    ticker = yf.Ticker(symbol)
    # You can access either 'regularMarketPrice' or 'currentPrice'
    info = ticker.info
    return info.get('regularMarketPrice', info.get('currentPrice')) 

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(get_yahoo_data('AAPL'))

