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

main_group = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Обменять ₽ - ¥', url = 'https://t.me/stefanswe1')]
])
