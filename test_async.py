import asyncio

async def print_after_two_secs():
    await asyncio.sleep(2)
    print("Hello")

async def print_world():
    print('world')
        
async def main():
    task1 = asyncio.create_task(print_after_two_secs())
    task2 = asyncio.create_task(print_world())
    await task1
    await task2

asyncio.run(main())