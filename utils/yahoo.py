import time
import random
import logging
from datetime import datetime, timezone
from multiprocessing import Queue
from queue import Empty
from typing import List

from yfinance import Ticker

@staticmethod
def _get_next_symbol(queue: Queue, output: List[Queue] | None = None):
    if output is not None and not isinstance(output, list):
        output = [output]
    
    while True:
        try:
            val = queue.get(timeout=10)
        except Empty:
            logging.warning('Queue timeout reached, stopping')
            break

        if val == 'DONE':
            logging.info('yahoo worker recieved "DONE"')
            break
        price = _get_yahoo_data(val)
        if output is not None:
            for out in output:
                out.put((val, price, datetime.now(timezone.utc)))
        logging.info(f"{val},{price}")
        time.sleep(10 * random.random())

    # if output is not None:
    #     for out in output:
    #         for _ in range(20):
    #             out.put('DONE')

@staticmethod
def _get_yahoo_data(symbol: str):
    ticker = Ticker(symbol)
    # You can access either 'regularMarketPrice' or 'currentPrice'
    info = ticker.info
    return info.get('regularMarketPrice', info.get('currentPrice')) 

@staticmethod
def run(queue: Queue, output: List[Queue]):
    return _get_next_symbol(queue, output)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(_get_yahoo_data('AAPL'))

