import random

from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import config
from databases import databases_functions
import app.text_messages as text
from bot_instance import bot

router = Router()


class RateChange(StatesGroup):
    currency = State()
    currency_rate = State()


class Change_rub(StatesGroup):
    quantity = State()


class Change_cny(StatesGroup):
    quantity = State()


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
    databases_functions.add_new_user(message.from_user.id)
    await message.answer(text.message, reply_markup=kb.main)


@router.message(Command('promo'))
async def cmd_promo(message: Message):
    promo = databases_functions.get_promo_user(message.from_user.id)
    await message.answer(
        f"{f'У Вас Применен промокод {promo[0]} на скику {promo[1]}' if promo is not None else 'ВВедите промокод'}",
        reply_markup=kb.main)


# Колхоз, но я испралю
@router.message(F.text == 'Обмен ₽ - ¥')
async def exchange_cny(message: Message):
    value_CNY = databases_functions.get_currency_value('CNY')
    promo = databases_functions.get_promo_user(message.from_user.id)
    print(type(promo[0]))
    await message.answer(
        f"{f"У Вас применен промокод: <b>{promo[0]}</b> на скидку {promo[1]}" if promo[1] != "0" else ""}\n"
        f"От 250¥ - {f'<s>{round(float(value_CNY) + 0.3, 2)}₽ </s>{round(float(value_CNY) + 0.3 - float(promo[1]), 2)}₽' if promo[1] != "0" else f'{round(float(value_CNY) + 0.3, 2)}₽'}\n"
        f"От 500¥ - {f'<s>{round(float(value_CNY) + 0.2, 2)}₽ </s>{round(float(value_CNY) + 0.2 - float(promo[1]), 2)}₽' if promo[1] != "0" else f'{round(float(value_CNY) + 0.2, 2)}₽'}\n"
        f"От 1000¥ - {f'<s>{round(float(value_CNY) + 0.1, 2)}₽ </s>{round(float(value_CNY) + 0.1 - float(promo[1]), 2)}₽' if promo[1] != "0" else f'{round(float(value_CNY) + 0.1, 2)}₽'}\n"
        f"От 2500¥ - {f'<s>{round(float(value_CNY) + 0.05, 2)}₽ </s>{round(float(value_CNY) + 0.05 - float(promo[1]), 2)}₽' if promo[1] != "0" else f'{round(float(value_CNY) + 0.05, 2)}₽'}\n"
        f"От 10000¥ - {f'<s>{round(float(value_CNY), 2)}₽ </s>{round(float(value_CNY) - float(promo[1]), 2)}₽' if promo[1] != "0" else f'{round(float(value_CNY), 2)}₽'}\n",
        reply_markup=kb.change_choice)


@router.callback_query(F.data == 'change_rub')
async def change_rub(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Change_rub.quantity)
    await callback.message.edit_text('Введите сумму в рублях, которую вы хотиите обменять')


def value_change(order_info):
    print(type(order_info["change_cny"]))
    if 250 < order_info["change_cny"] < 500:
        return 0.3
    elif 499 < order_info["change_cny"] < 1000:
        return 0.2
    elif 999 < order_info["change_cny"] < 2500:
        return 0.1
    elif 2499 < order_info["change_cny"] < 10000:
        return 0.05
    elif 9999 < order_info["change_cny"]:
        return 0


# Колхоз, но я испралю
@router.message(Change_rub.quantity)
async def change_rub_cny(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите числовое значение.")
        return
    await state.update_data(quantity=int(message.text))
    promo = float(databases_functions.get_promo_user(message.from_user.id)[1])
    value_CNY = float(databases_functions.get_currency_value('CNY'))
    await state.update_data(rate=round(value_CNY - promo, 2))
    await state.update_data(change_cny=round(int(message.text) // value_CNY - promo, 2))
    order_info = await state.get_data()

    async def send_message(overpayment):
        order_info.update(rate=round(value_CNY - promo + overpayment, 2))
        order_info.update(change_cny=int(int(message.text) // (value_CNY - promo + overpayment)))
        order_info.update({'order_id': random.randint(100000, 999999999)})
        databases_functions.add_order(order_info["order_id"], message.from_user.id, message.from_user.username,
                                      order_info["quantity"], order_info["rate"],
                                      order_info["change_cny"])
        await message.answer(
            f"Вы хотите обменять {order_info['quantity']} по курсу {order_info['rate']}, на {order_info["change_cny"]}",
            reply_markup=kb.approve_change)

    if order_info["change_cny"] < 250:
        await message.answer("Мы не обмениваем меньше 250¥")
        await state.clear()
    else:
        await send_message(value_change(order_info))
    await state.clear()


@router.callback_query(F.data == 'change_cny')
async def change_rub(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(Change_cny.quantity)
    await callback.message.edit_text('Введите сумму в юанях, которую вы хотиите обменять')


@router.message(Change_cny.quantity)
async def change_rub_cny(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите числовое значение.")
        return
    await state.update_data(change_cny=int(message.text))
    promo = float(databases_functions.get_promo_user(message.from_user.id)[1])
    value_CNY = float(databases_functions.get_currency_value('CNY'))
    await state.update_data(rate=round(value_CNY - promo, 2))
    order_info = await state.get_data()

    async def send_message(overpayment):
        order_info.update(rate=round(value_CNY - promo + overpayment, 2))
        order_info.update(quantity=int(int(message.text) * (value_CNY - promo + float(overpayment))))
        order_info.update({'order_id': random.randint(100000, 999999999)})
        databases_functions.add_order(order_info["order_id"], message.from_user.id, message.from_user.username,
                                      order_info["quantity"], order_info["rate"],
                                      order_info["change_cny"])
        await message.answer(
            f"Вы хотите обменять {order_info['quantity']} по курсу {order_info['rate']}, на {order_info["change_cny"]}",
            reply_markup=kb.approve_change)

    if order_info["change_cny"] < 250:
        await message.answer("Мы не обмениваем меньше 250¥")
        await state.clear()
    else:
        await send_message(value_change(order_info))
    await state.clear()


@router.message(F.text == 'Подтвердить ✅')
async def approve_exchange(message: Message):
    order = databases_functions.get_last_order(message.from_user.id)
    databases_functions.approve_order(message.from_user.id)
    await message.answer(text="cоси хуй ", reply_markup=kb.main)
    print(order)
    await bot.send_message(chat_id='585296404', text='asd')
