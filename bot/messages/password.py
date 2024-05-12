
import logging
from aiogram import Dispatcher,types,F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from aiogram.filters import Command,StateFilter
import utils


def register_handlers(dp : Dispatcher):
    dp.message.register(verify_pass, Command('verify_password'))
    dp.message.register(process_pass, StateFilter(PasswordStates.check_password))

    logging.info('Regisered PASSWORD handlers')

class PasswordStates(StatesGroup):
    check_password = State()

async def verify_pass(message: types.Message, state: FSMContext):
    await message.answer('Введите пароль для проверки')
    await state.set_state(PasswordStates.check_password)

async def process_pass(message: types.Message, state: FSMContext):
    password = utils.verify_password(message.text)

    if password:
        text = 'Пароль сильный'
    else:
        text = 'Пароль слабый'

    await message.answer(text)
    await state.set_state()
