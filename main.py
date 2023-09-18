from logic.main import run
import asyncio
import random
from notifications.telegram import send_telegram_message

async def main():
    # report a message
    print('main coroutine started')
    # get the current event loop
    loop = asyncio.get_event_loop()
    # create and schedule the task
    task = loop.create_task(execute())
    # wait for the task to complete
    await task
    # report a final message
    print('main coroutine done')

async def execute():
  while True:
    send_telegram_message('\nExecuting...')
    await run("football")
    await asyncio.sleep(5)
    await run("tennis")
    # Schedule the task to be run again in 40-70 seconds
    seconds_to_wait = random.randint(123, 341)
    send_telegram_message('\nEnded execution, waiting ' + str(seconds_to_wait) + ' seconds to run again')
    await asyncio.sleep(seconds_to_wait)

if __name__ == '__main__':
  asyncio.run(main())