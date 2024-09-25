import sqlite3


def add_or_update_currency(currency_name, value):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\currencyRate.db') as conn:
        cursor = conn.cursor()

        # Проверяем, существует ли валюта
        cursor.execute('SELECT * FROM currencyRate WHERE currency = ?', (currency_name,))
        result = cursor.fetchone()

        if result is None:
            # Если не существует, создаем новую запись
            cursor.execute('INSERT INTO currencyRate (currency, value) VALUES (?, ?)', (currency_name, value))
        else:
            # Если существует, обновляем значение
            cursor.execute('UPDATE currencyRate SET value = ? WHERE currency = ?', (value, currency_name))

        # Сохраняем изменения
        conn.commit()


def get_currency_value(currency_name):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\currencyRate.db') as conn:
        cursor = conn.cursor()

        # Извлекаем значение для указанной валюты
        cursor.execute('SELECT value FROM currencyRate WHERE currency = ?', (currency_name,))
        result = cursor.fetchone()

        if result is not None:
            return result[0]  # Возвращаем значение
        else:
            return None  # Если валюта не найдена


def get_promo_user(userId):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\users_with_promo.db') as conn:
        cursor = conn.cursor()

        # Извлекаем значение для указанной валюты
        cursor.execute('SELECT promo, value FROM users_with_promo WHERE userId = ?', (userId,))
        result = cursor.fetchone()

        if result is not None:
            return result  # Возвращаем значение
        else:
            return None  # Если валюта не найдена
