import threading

counter = 0

def increament():
    global counter
    for i in range(10**8):
        counter+=1

threads = []
for i in range(4):
    x = threading.Thread(target=increament)
    threads.append(x)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

print(f"counter value: {counter}")
