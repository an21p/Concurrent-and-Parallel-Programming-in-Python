import time

from workers.Worker import Worker

def calc_sum_sq(n):
    sum_sq = 0
    for i in range(n):
        sum_sq += i ** 2
    print(sum_sq)

def sleep_n(n):
    time.sleep(n)

def main():
    ## cpu intensive (no improvement - consider multiprocess)
    thread_list = []
    calc_start = time.time()
    for i in range(5):
        input = (i+1) * 1_000_000
        worker = Worker(func=calc_sum_sq, args=(input,))
        thread_list.append(worker)

    for tt in thread_list:
        tt.join()
    
    print('Calc: ', round(time.time() - calc_start, 1))

    ## io intesive (good imporvement)
    thread_list = []
    sleep_start = time.time()
    for i in range(1, 6):
        worker = Worker(func=sleep_n, args=(i,))
        thread_list.append(worker)

    for tt in thread_list:
        tt.join()
        
    print('Sleep: ', round(time.time() - sleep_start, 1))

if __name__ == '__main__':
    main()
