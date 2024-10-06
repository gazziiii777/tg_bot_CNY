from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

admin = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Создать промокод')],
    [KeyboardButton(text='Посмотреть промокоды')],
    [KeyboardButton(text='Поменять курс валюты')],
], resize_keyboard=True, input_field_placeholder="Можно текст")

admin_approve_currency_change = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Поддвердить изменение цены')],
    [KeyboardButton(text='Отменить')],
], resize_keyboard=True, input_field_placeholder="Можно текст")

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Обмен ₽ - ¥')],
    [KeyboardButton(text='Обмен других валют'), KeyboardButton(text='Обучение')],
    [KeyboardButton(text='Справка'), KeyboardButton(text='Отзывы')],
], resize_keyboard=True, input_field_placeholder="Можно текст")

change_choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Ввести сумму в рублях', callback_data='change_rub')],
    [InlineKeyboardButton(text='Ввести сумму в юанях', callback_data='change_cny')],
])

approve_change = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Подтвердить ✅')],
    [KeyboardButton(text='Отмена'), KeyboardButton(text='Отзывы')],
], resize_keyboard=True, input_field_placeholder="Можно текст")

