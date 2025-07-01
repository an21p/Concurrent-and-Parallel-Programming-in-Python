
import asyncio
import time

async def async_sleep(n):
    print(f"Before {n}")
    await asyncio.sleep(5)
    print(f"After {n}")

async def hello():
    print("Hello1")

async def return_hello():
    return "Hello2"

async def main():
    start = time.time()
    task = asyncio.create_task(async_sleep(1))
    await async_sleep(2)
    await task
    result = await return_hello()
    print(result)
    print(f"total time: {time.time() - start}")


# Can have one running event-loop per thread
# 1 thread
# 1 core
if __name__ == '__main__':
    asyncio.run(main())

