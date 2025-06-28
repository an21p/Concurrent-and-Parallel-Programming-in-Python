import time
import threading

def calc_sum_sq(n):
    sum_sq = 0
    for i in range(n):
        sum_sq += i ** 2

    print(sum_sq)


def sleep_n(n):
    time.sleep(n)


def main():
    calc_start = time.time()
    for i in range(5):
        input = (i+1) * 1_000_000
        calc_sum_sq(input)

    print('Calc: ', round(time.time() - calc_start, 1))

    sleep_start = time.time()
    for i in range(1, 6):
        sleep_n(i)

    print('Sleep: ', round(time.time() - sleep_start, 1))


def threads():
    ## cpu intensive (no improvement - consider multiprocess)
    thread_list = []
    calc_start = time.time()
    for i in range(5):
        input = (i+1) * 1_000_000
        t = threading.Thread(target=calc_sum_sq, args=(input,))
        t.start()
        thread_list.append(t)

    for tt in thread_list:
        tt.join()
    
    print('Calc: ', round(time.time() - calc_start, 1))

   ## io intesive (good imporvement)
    thread_list = []
    sleep_start = time.time()
    for i in range(1, 6):
        t = threading.Thread(target=sleep_n, args=(i,))
        t.start()
        thread_list.append(t)

    for tt in thread_list:
        tt.join()

    print('Sleep: ', round(time.time() - sleep_start, 1))

if __name__ == '__main__':
    main()
    threads()
