import sqlite3


def add_new_user(user_id):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\users.db') as conn:
        cursor = conn.cursor()

        # Проверяем, существует ли валюта
        cursor.execute('SELECT * FROM users WHERE userId = ?', (user_id,))
        result = cursor.fetchone()

        if result is None:
            # Если не существует, создаем новую запись
            cursor.execute('INSERT INTO users (userId, promo, value) VALUES (?, ?, ?)', (user_id, 0, 0))

        # Сохраняем изменения
        conn.commit()


def add_or_update_currency(currency_name, value):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\users.db') as conn:
        cursor = conn.cursor()

        # Проверяем, существует ли валюта
        cursor.execute('SELECT * FROM currency_rate WHERE currency = ?', (currency_name,))
        result = cursor.fetchone()

        if result is None:
            # Если не существует, создаем новую запись
            cursor.execute('INSERT INTO currency_rate (currency, value) VALUES (?, ?)', (currency_name, value))
        else:
            # Если существует, обновляем значение
            cursor.execute('UPDATE currency_rate SET value = ? WHERE currency = ?', (value, currency_name))

        # Сохраняем изменения
        conn.commit()


def get_currency_value(currency_name):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\users.db') as conn:
        cursor = conn.cursor()

        # Извлекаем значение для указанной валюты
        cursor.execute('SELECT value FROM currency_rate WHERE currency = ?', (currency_name,))
        result = cursor.fetchone()

        if result is not None:
            return result[0]  # Возвращаем значение
        else:
            return None  # Если валюта не найдена


def get_promo_user(userId):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\users.db') as conn:
        cursor = conn.cursor()

        # Извлекаем значение для указанной валюты
        cursor.execute('SELECT promo, value FROM users WHERE userId = ?', (userId,))
        result = cursor.fetchone()

        if result is not None:
            return result  # Возвращаем значение
        else:
            return None  # Если валюта не найдена


def add_order(order_id, user_id, user_username, quantity, exchange_rate, change_cny):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\users.db') as conn:
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO orders (order_id, user_id, user_username, quantity, exchange_rate, change_cny) VALUES (?, ?, ?, ?, ?, ?)',
            (order_id, user_id, user_username, quantity, exchange_rate, change_cny))
        conn.commit()


def get_last_order(user_id):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE user_id = ? AND approve IS NULL', (user_id,))
        result = cursor.fetchone()
        return result


def approve_order(user_id):
    with sqlite3.connect(r'D:\pythonProject\tg_bot_CNY\databases\users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE orders SET approve = ? WHERE user_id = ?', ('yes', user_id,))
        conn.commit()
