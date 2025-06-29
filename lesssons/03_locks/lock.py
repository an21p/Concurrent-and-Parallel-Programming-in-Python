import threading

counter = 0

lock = threading.Lock()

def increament():
    global counter
    for i in range(10**6):
        # lock.acquire()
        with lock:
            counter+=1
        # lock.release()

threads = []
for i in range(4):
    x = threading.Thread(target=increament)
    threads.append(x)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"counter value: {counter}")
