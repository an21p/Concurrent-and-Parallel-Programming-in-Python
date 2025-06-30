from multiprocessing import Pool, cpu_count
import time

def square(x,y,a):
    return x ** y + a

if __name__ == "__main__":
    num_cpu_available = max(1, cpu_count() - 1)
    print(num_cpu_available)
    num_processes = 4

    comparison_list = [10,20,30]
    power = [2,1,2]
    extra = [10,-40,-100]

    start_time = time.time()

    prepared_list = []
    for i in range(len(comparison_list)):
        prepared_list.append((comparison_list[i], power[i], extra[i]))

    with Pool(2) as mp_pool:
        result = mp_pool.starmap(square, prepared_list)

    print(result)
    print(f"Time: {time.time() - start_time} seconds")
