from logic.main import run
import asyncio
import random
import time
from notifications.telegram import send_telegram_message


async def main():
    # report a message
    print('main coroutine started')
    # get the current event loop
    loop = asyncio.get_event_loop()
    # create and schedule the task
    loop.create_task(execute())
    task = loop.create_task(is_alive())
    # wait for the task to complete
    await task
    # report a final message
    print('main coroutine done')


async def is_alive():
    send_telegram_message('Started...')
    while True:
        await asyncio.sleep(3600)
        send_telegram_message('Still alive...')


async def execute():
    while True:
        try:
            print('\nrunning for football')
            start_time = time.time()
            await run("football")
            end_time = time.time()
            elapsed_time = end_time - start_time
            print('football done')
            print("elapsed time: {:.2f}s".format(elapsed_time))


        except Exception as ex:
            print('football exception')
            print(str(ex))

        await asyncio.sleep(5)

        try:
            print('\nrunning for tennis')
            start_time = time.time()
            await run("tennis")
            end_time = time.time()
            elapsed_time = end_time - start_time
            print('tennis done')
            print("elapsed time: {:.2f}s".format(elapsed_time))

        except Exception as ex:
            print('tennis exception')
            print(str(ex))
        # Schedule the task to be run again in 40-70 seconds
        seconds_to_wait = random.randint(123, 341)
        await asyncio.sleep(seconds_to_wait)


if __name__ == '__main__':
    asyncio.run(main())
