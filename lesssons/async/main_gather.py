
import asyncio
import time

async def async_sleep(n):
    print(f"Before {n}")
    await asyncio.sleep(n)
    print(f"After {n}")

async def hello():
    print("Hello1")

async def return_hello():
    return "Hello2"

async def main():
    start = time.time()

    first = asyncio.wait_for( async_sleep(30),5) 

    try: 
        await asyncio.gather(first , async_sleep(1), hello())
    except asyncio.TimeoutError:
        print('Timeout')

    print(f"total time: {time.time() - start}")


# Can have one running event-loop per thread
# 1 thread
# 1 core
if __name__ == '__main__':
    asyncio.run(main())

