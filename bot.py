import asyncio
import logging
import os
from misc import bot,dp
from messages.register_handlers import register_messages_handlers
import subprocess

async def main():
    register_messages_handlers(dp)
    logging.info('Starting bot')

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
