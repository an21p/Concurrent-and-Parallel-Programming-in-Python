from multiprocessing import Process, Pool, cpu_count
from functools import partial
import time

def square(y,a,x):
    return x ** y + a

if __name__ == "__main__":
    num_cpu_available = max(1, cpu_count() - 1)
    print(num_cpu_available)
    num_processes = 4

    comparison_list = [10,20,30]
    power = 2
    partial_function = partial(square, power, 10)

    start_time = time.time()

    with Pool(2) as mp_pool:
        result = mp_pool.map(partial_function, comparison_list)

    print(result)
    print(f"Time: {time.time() - start_time} seconds")
