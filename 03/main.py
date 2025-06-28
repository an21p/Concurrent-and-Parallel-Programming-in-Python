import time

from worker.Worker import Worker
from utils.wiki import get_sp_500_companies
from utils.yahoo import get_next_symbol
from utils.db import store_next_symbol
from multiprocessing import Queue
import logging

def main() -> None:
    start_time = time.time()

    symbol_queue = Queue()
    db_queue = Queue()

    yahoo_worker_count = 5
    db_worker_count = 2

    workers = []
    db_workers = []

    for _ in range(yahoo_worker_count):
        workers.append(Worker(get_next_symbol, (symbol_queue, [db_queue])))

    for _ in range(db_worker_count):
        db_workers.append(Worker(store_next_symbol, (db_queue,)))

    count = 0
    for symbol in get_sp_500_companies():
        symbol_queue.put(symbol)
        count+=1
        if count > 5:
            break

   
    for _ in workers:
        symbol_queue.put('DONE') 

    for worker in workers:
        worker.join()

    for worker in db_workers:
        worker.join()

    logging.info("Main time: ", time.time() - start_time)

if __name__ == '__main__':
    main()
