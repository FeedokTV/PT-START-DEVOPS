import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from db import init_db

load_dotenv(override=True)

logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('aiogram').setLevel(logging.WARNING)

allowed_commands = []

db = init_db()

bot = Bot(token=os.environ['TOKEN'])
dp = Dispatcher(storage=MemoryStorage())