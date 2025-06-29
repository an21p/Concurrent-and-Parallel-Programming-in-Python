import importlib
import yaml
import time
import logging
import threading
from multiprocessing import Queue
from worker.Worker import Worker
from typing import Dict,List

class YamlPipelineExecutor(threading.Thread):
    def __init__(self, pipeline_location: str):
        super(YamlPipelineExecutor, self).__init__()
        self._pipeline_location: str = pipeline_location
        self._queues: Dict[str, Queue] = {}
        self._workers: Dict[str, List[Worker]] = {}
        self._queue_consumers = {}
        self._downstream_queues = {}

    def _load_pipeline(self):
        with open(self._pipeline_location, 'r') as f:
            self._yaml_data = yaml.safe_load(f)

    def _initialise_queues(self):
        for queue in self._yaml_data["queues"]:
            name = queue['name']
            self._queues[name] = Queue()

    def _initialise_workers(self):
        for worker in self._yaml_data["workers"]:
            name = worker['name']
            run_func = getattr(importlib.import_module(worker['location']), 'run')
            input_queue_name = worker.get('input_queue', None)
            output_queues_names = worker.get('output_queues', [])
            instances = worker.get('instances', 1)

            self._downstream_queues[name] = output_queues_names
            if input_queue_name is not None:
                self._queue_consumers[input_queue_name] = instances # one pipeline item per queue

            input_queue = self._queues[input_queue_name] if input_queue_name is not None and input_queue_name in self._queues else None
            output_queues = []
            for output_queue_name in output_queues_names:
                if output_queue_name in self._queues:
                    output_queues.append(self._queues[output_queue_name])

            # wiki
            input_values = worker.get('input_values')
            input_queue = input_values if input_values is not None else input_queue
            
            self._workers[name] = [Worker(run_func, (input_queue, output_queues)) for _ in range(instances)]

    def _join_workers(self):
        for worker_name in self._workers:
            for worker_thread in self._workers[worker_name]:
                worker_thread.join()


    def process_pipeline(self):
        start_time = time.time()
        self._load_pipeline()
        self._initialise_queues()
        self._initialise_workers()
        # self._join_workers()
        logging.info(f"Main time: {time.time() - start_time}")

    def run(self):
        self.process_pipeline()
        while True:
            total_workers_alive = 0
            worker_stats = []
            to_del = []
            for worker_name in self._workers:
                total_worker_threads_alive = 0
                for worker_thread in self._workers[worker_name]:
                    if worker_thread.is_alive():
                        total_worker_threads_alive+=1
                total_workers_alive += total_worker_threads_alive
                if total_worker_threads_alive == 0:
                    if self._downstream_queues[worker_name] is not None:
                        for output_queue in self._downstream_queues[worker_name]:
                            number_of_consumers = self._queue_consumers[output_queue]
                            for _ in range(number_of_consumers):
                                self._queues[output_queue].put('DONE')
                    to_del.append(worker_name)
                worker_stats.append([worker_name, total_workers_alive])
            logging.info(worker_stats)
            if total_workers_alive == 0:
                break

            for worker_name in to_del:
                del self._workers[worker_name]
            time.sleep(5)
