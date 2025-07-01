import asyncio
import random
import time

async def async_sleep(duration):
    await asyncio.sleep(duration)
    return duration


async def main():
    start_time = time.time()
    pending = set()
    for i in range(1, 11):
        pending.add(asyncio.create_task(async_sleep(random.random()*30)))

    while len(pending)>0:
        done, pending = await asyncio.wait(pending, timeout=2)
        # done, pending = await asyncio.wait(pending, return_when="ALL_COMPLETED")
        # done, pending = await asyncio.wait(pending, return_when="FIRST_COMPLETED")
        print(f"\nTime Elapsed: {time.time() - start_time}\nDone: {len(done)}\nPending: {len(pending)}")

        for done_task in done:
            print(await done_task)



if __name__ == "__main__":
    asyncio.run(main())
