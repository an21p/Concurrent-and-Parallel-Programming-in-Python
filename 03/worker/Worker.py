import threading

class Worker(threading.Thread):
    def __init__(self, func, args, **kwargs):
        super(Worker, self).__init__(**kwargs)
        self._func = func
        self._args = args
        self.start()

    def run(self):
        self._func(*self._args)
