
import logging
import os
import subprocess
from aiogram import Dispatcher,types,F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from aiogram.filters import Command,StateFilter
import utils
from misc import db


def register_handlers(dp : Dispatcher):
    dp.message.register(get_info, F.text.startswith('/get_'))

    logging.info('Regisered SYSTEM handlers')

async def get_info(message: types.Message, state: FSMContext):
    splitted_command = message.text.split(' ')
    if len(splitted_command) > 1:
        command = message.text.split(' ')[0][5:]
        subcommand = message.text.split(' ')[1]
    else:
        command = message.text.split(' ')[0][5:]
        subcommand = None
    
    if command == 'release':
        result = utils.run_command('lsb_release -a')
    elif command == 'uname':
        result = utils.run_command('uname -a')
    elif command == 'uptime':
        result = utils.run_command('uptime')
    elif command == 'df':
        result = utils.run_command('df -h')
    elif command == 'free':
        result = utils.run_command('free -h')
    elif command == 'mpstat':
        result = utils.run_command('mpstat')
    elif command == 'w':
        result = utils.run_command('w')
    elif command == 'auths':
        result = utils.run_command('last -n 10')
    elif command == 'critical':
        result = utils.run_command('journalctl -p 0..3 -n 5')
    elif command == 'ps':
        result = utils.run_command('ps aux | head -n 10')
    elif command == 'ss':
        result = utils.run_command('ss -t')
    elif command == 'apt_list':
        if subcommand == None:
            result = utils.run_command('apt list --installed | head -n 25')
        else:
            result = utils.run_command(f'apt show {subcommand}')
    elif command == 'services':
        result = utils.run_command('systemctl list-units --type=service | head -n 25')
    elif command == 'emails':
        db.execute("SELECT * FROM emails;")
        data = db.fetchall()
        result = 'id\t\t\temail\n'
        for row in data:
            result += ''.join([str(row[0]),'\t\t\t',row[1],'\n'])
    elif command == 'phone_numbers':
        db.execute("SELECT * FROM phone_numbers;")
        data = db.fetchall()
        result = 'id\t\t\tphone_number\n'
        for row in data:
            result += ''.join([str(row[0]),'\t\t\t',row[1],'\n'])
    elif command == 'repl_logs':
        result = utils.run_command(f"echo {os.environ['RM_PASSWORD']} | sudo -S tail /var/log/postgresql/postgresql-14-main.log -n 25")

    text = 'Результат выполнения команды:\n'
    text += result

    await message.answer(text)