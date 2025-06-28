import importlib
import yaml
import time
import logging
import os
from multiprocessing import Queue
from worker.Worker import Worker
from typing import Dict,List

class YamlPipelineExecutor:
    def __init__(self, pipeline_location: str):
        self._pipeline_location: str = pipeline_location
        self._queues: Dict[str, Queue] = {}
        self._workers: Dict[str, List[Worker]] = {}

    def _load_pipeline(self):
        print(os.getcwd())
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
        self._join_workers()
        logging.info(f"Main time: {time.time() - start_time}")
