from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton

set_city_kb = InlineKeyboardBuilder(
    markup= [
        [InlineKeyboardButton(text = 'Бишкек',callback_data='city_set_bishkek'),
        InlineKeyboardButton(text = 'Иссык-Куль',callback_data='city_set_ik')]
    ]   
)
profile_kb = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Изменить профиль',callback_data='update_profile')],
        [InlineKeyboardButton(text = 'Переключить язык',callback_data='switch_language')]
    ]
)

default_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Отслеживание'),
            KeyboardButton(text = 'Поддержка'),
        ],
        [
            KeyboardButton(text = 'Профиль'),
            KeyboardButton(text = 'Адреса'),
        ],
        [
            KeyboardButton(text = 'Инструкция'),
            KeyboardButton(text = 'Калькулятор'),
        ]
    ],
    resize_keyboard=True
)

cancel_calc = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text = 'Отмена')
        ]
    ],
    resize_keyboard=True
)

tracking_kb = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'По трек-коду',callback_data = 'track-code')],
        [InlineKeyboardButton(text = 'По коду клиента',callback_data='client_id')]
    ]
)

admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Таблица с отправленными с Китая'),
            KeyboardButton(text = 'Таблица с прибывшими в КР')
        ]
    ],
    resize_keyboard=True
)