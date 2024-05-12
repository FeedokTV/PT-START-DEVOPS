
import logging
from aiogram import Dispatcher,types,F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from aiogram.filters import Command,StateFilter
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import utils
import ast
from misc import db,bot


def register_handlers(dp : Dispatcher):
    dp.message.register(start, Command('start'))
    dp.message.register(help, Command('help'))
    dp.message.register(find_emails, Command('find_emails'))
    dp.message.register(process_emails, StateFilter(SearchStates.search_email))
    dp.message.register(find_phone_numbers, Command('find_phone_numbers'))
    dp.message.register(process_phone_numbers, StateFilter(SearchStates.search_phone_numbers))
    dp.callback_query.register(add_to_db,F.data.startswith('add_to_db_'))
    dp.callback_query.register(finish_search,F.data=='finish_search')

    logging.info('Regisered SEARCH handlers')

class SearchStates(StatesGroup):
    search_email = State()
    search_phone_numbers = State()

async def start(message: types.Message, state: FSMContext):
    await message.answer("Я могу помочь найти email или номер телефона, дам информацию о своём сервере и проверю твой пароль на сложность")

async def help(message: types.Message, state: FSMContext):
    text = '/find_emails - найти <b>Email</b>\n' + \
            '/find_phone_numbers - найти <b>номер телефона</b>\n\n' + \
            '/verify_password - проверка сложности пароля\n\n' + \
            '<b>Сбор информации о системе:</b>\n' + \
            '/get_release - релиз\n/get_uname - архитектура процессора, имя хоста системы и версия ядра\n' + \
            '/get_uptime - время работы\n' + \
            '/get_df - Сбор информации о состоянии файловой системы\n' + \
            '/get_free - Сбор информации о состоянии оперативной памяти\n' + \
            '/get_mpstat - Сбор информации о производительности системы\n' + \
            '/get_w - Сбор информации о работающих в данной системе пользователях\n' + \
            '<b>Сбор логов</b>\n' + \
            '/get_auths - Последние 10 входов в систему\n' + \
            '/get_critical - Последние 5 критических событий\n' + \
            '/get_critical - Сбор информации о запущенных процессах\n' + \
            '/get_ss - Сбор информации об используемых портах\n' + \
            '/get_apt_list - Сбор информации об установленных пакетах\n' + \
            "/get_apt_list [имя пакета] - Сбор информации об указанном пакете\n" + \
            '/get_services - Сбор информации о запущенных сервисах' + \
            '<b>База данных</b>\n' + \
            '/get_repl_logs - данные репликации и логи\n' + \
            '/get_emails - показать список email из БД\n' + \
            '/get_phone_numbers - показать список номеров телефонов из БД\n'
    await message.answer(text, parse_mode='HTML')

async def find_emails(message: types.Message, state: FSMContext):
    await message.answer('Введите текст для поиска')
    await state.set_state(SearchStates.search_email)

async def process_emails(message: types.Message, state: FSMContext):
    emails = utils.find_emails(message.text)

    if not(emails):
        await message.answer('Email адреса не найдены')
        await state.set_state()
        return

    text = "Найденные email-адреса:\n" + "\n".join(emails) + "\n"
    text += 'Желаете добавить новые в базу данных?'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да',callback_data='add_to_db_email'),InlineKeyboardButton(text='Нет',callback_data='finish_search')]
    ])

    await state.update_data(current_list=str(emails))

    await message.answer(text,reply_markup=keyboard)
    await state.set_state()

async def find_phone_numbers(message: types.Message, state: FSMContext):
    await message.answer('Введите текст для поиска')
    await state.set_state(SearchStates.search_phone_numbers)

async def process_phone_numbers(message: types.Message, state: FSMContext):
    phone_numbers = utils.find_phone_numbers(message.text)

    if not(phone_numbers):
        await message.answer('Телефонные адреса не найдены')
        await state.set_state()
        return

    text = "Найденные телефонные адреса:\n" + "\n".join(phone_numbers) + "\n"
    text += 'Желаете добавить новые в базу данных?'

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Да',callback_data='add_to_db_phone_numbers'),InlineKeyboardButton(text='Нет',callback_data='finish_search')]
    ])

    await state.update_data(current_list=str(phone_numbers))

    await message.answer(text,reply_markup=keyboard)
    await state.set_state()

async def add_to_db(callback: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    insert_list = ast.literal_eval(user_data['current_list'])
    result = ''
    if callback.data == 'add_to_db_email':
        for email in insert_list:
            # Check if not exists
            logging.info(f'Searching in emails table for {email}')
            db.execute(f"SELECT email FROM emails WHERE email = '{email}'")
            if db.fetchone() is None:
                try:
                    logging.info(f'Inserting in emails table {email}')
                    db.execute(f"INSERT INTO emails (email) VALUES ('{email}');")
                except Exception as e:
                    logging.error(str(e))
                    result += f'{email} - строка не добавлена, проверьте ошибку в логах'
        
        result += 'Данные обновлены!'
    else:
        for phone_number in insert_list:
            # Check if not exists
            if phone_number.startswith('8'):
                phone_number = '+7' + phone_number[1:]
            logging.info(f'Searching in numbers table for {phone_number}')
            db.execute(f"SELECT phone_number FROM phone_numbers WHERE phone_number = '{phone_number}'")
            if db.fetchone() is None:
                try:
                    logging.info(f'Inserting in numbers table {phone_number}')
                    db.execute(f"INSERT INTO phone_numbers (phone_number) VALUES ('{phone_number}');")
                except Exception as e:
                    result += f'{phone_number} - строка не добавлена, проверьте ошибку в логах'
                    logging.error(str(e))
        result += 'Данные обновлены!'
    
    await callback.message.answer(result)
    await bot.answer_callback_query(callback.id)

async def finish_search(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text('Поиск закончен')