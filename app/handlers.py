from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import config
from databases import databases_functions
import app.text_messages as text

router = Router()


class RateChange(StatesGroup):
    currency = State()
    currency_rate = State()


# Команды Админа
@router.message(Command('admin'))
async def cmd_start(message: Message):
    print(message.from_user.id)
    if str(message.from_user.id) in config.ADMINS_ID:
        await message.answer("Панель админа", reply_markup=kb.admin)


@router.message(F.text == 'Поменять курс валюты')
async def change_currency_rate(message: Message, state: FSMContext):
    if str(message.from_user.id) in config.ADMINS_ID:
        await state.set_state(RateChange.currency)
        await message.answer('Введите название валюты, пример: CNY')


@router.message(RateChange.currency)
async def currencyRate(message: Message, state: FSMContext):
    if str(message.from_user.id) in config.ADMINS_ID:
        await state.update_data(currency=message.text)
        await state.set_state(RateChange.currency_rate)
        await message.answer('Введите название валюты, пример: 13.5 (Обязательно точка)')


@router.message(RateChange.currency_rate)
async def currencyRate(message: Message, state: FSMContext):
    if str(message.from_user.id) in config.ADMINS_ID:
        await state.update_data(currency_rate=message.text)
        global data
        data = await state.get_data()
        await message.answer(f'Все верно?\nНазвание валюты: {data["currency"]}\nКурс: {data["currency_rate"]}',
                             reply_markup=kb.admin_approve_currency_change)
        await state.clear()


@router.message(F.text == 'Поддвердить изменение цены')
async def exchange_cny(message: Message):
    if str(message.from_user.id) in config.ADMINS_ID and data != []:
        if '.' in data["currency_rate"]:
            databases_functions.add_or_update_currency(data["currency"], data["currency_rate"])
            await message.answer("Изменения применнены", reply_markup=kb.admin)
            data.clear()
        else:
            await message.answer("Изменения не применнеы, цена дожна содержать точку", reply_markup=kb.admin)
            data.clear()


@router.message(F.text == 'Отменить')
async def exchange_cny(message: Message):
    if str(message.from_user.id) in config.ADMINS_ID:
        await message.answer("Отменено", reply_markup=kb.admin)
        data.clear()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text.message, reply_markup=kb.main)


@router.message(Command('promo'))
async def cmd_promocode(message: Message):
    promo = databases_functions.get_promo_user(message.from_user.id)
    await message.answer(
        f"{f'У Вас Применен промокод {promo[0]} на скику {promo[1]}' if promo is not None else 'ВВедите промокод'}",
        reply_markup=kb.main)


@router.message(F.text == 'Обмен ₽ - ¥')
async def exchange_cny(message: Message):
    value_CNY = databases_functions.get_currency_value('CNY')
    promo = databases_functions.get_promo_user(message.from_user.id)
    await message.answer(
        f"{f"У Вас применен промокод: <b>{promo[0]}</b> на скидку {promo[1]}" if promo is not None else ""}\n"
        f"От 250¥ - {f'<s>{round(float(value_CNY) + 0.3, 2)}₽ </s>{round(float(value_CNY) + 0.3 - float(promo[1]), 2)}₽' if promo is not None else f'{round(float(value_CNY) + 0.3, 2)}₽'}\n"
        f"От 500¥ - {f'<s>{round(float(value_CNY) + 0.2, 2)}₽ </s>{round(float(value_CNY) + 0.2 - float(promo[1]), 2)}₽' if promo is not None else f'{round(float(value_CNY) + 0.2, 2)}₽'}\n"
        f"От 1000¥ - {f'<s>{round(float(value_CNY) + 0.1, 2)}₽ </s>{round(float(value_CNY) + 0.1 - float(promo[1]), 2)}₽' if promo is not None else f'{round(float(value_CNY) + 0.1, 2)}₽'}\n"
        f"От 2500¥ - {f'<s>{round(float(value_CNY) + 0.05, 2)}₽ </s>{round(float(value_CNY) + 0.05 - float(promo[1]), 2)}₽' if promo is not None else f'{round(float(value_CNY) + 0.05, 2)}₽'}\n"
        f"От 10000¥ - {f'<s>{round(float(value_CNY), 2)}₽ </s>{round(float(value_CNY) - float(promo[1]), 2)}₽' if promo is not None else f'{round(float(value_CNY), 2)}₽'}\n",
        reply_markup=kb.main_group)
