import time

from worker.Worker import Worker
from utils.wiki import run as wiki_run
from utils.yahoo import run as yahoo_run
from utils.db import run as db_run
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
        workers.append(Worker(yahoo_run, (symbol_queue, [db_queue])))

    for _ in range(db_worker_count):
        db_workers.append(Worker(db_run, (db_queue,)))

    count = 0
    for symbol in wiki_run():
        symbol_queue.put(symbol)
        count+=1
        if count > 3:
            break
   
    for _ in workers:
        symbol_queue.put('DONE') 

    for worker in workers:
        worker.join()

    for worker in db_workers:
        worker.join()

    logging.info(f"Main time: {time.time() - start_time}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
