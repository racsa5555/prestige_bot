from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton

language_kb = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = '🇷🇺',callback_data='RU'),
        InlineKeyboardButton(text = '🇰🇬',callback_data='KG')]
    ]
)

set_city_kb = InlineKeyboardBuilder(
    markup= [
        [InlineKeyboardButton(text = 'Бишкек',callback_data='city_set_bishkek'),
        InlineKeyboardButton(text = 'Иссык-Куль',callback_data='city_set_ik')]
    ]   
)
profile_kb_ru = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Изменить профиль',callback_data='update_profile')],
        [InlineKeyboardButton(text = 'Переключить язык',callback_data='switch_language')]
    ]
)
profile_kb_kg = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Профилди өзгөртүү',callback_data='update_profile')],
        [InlineKeyboardButton(text = 'Тилди өзгөртүү',callback_data='switch_language')]
    ]
)

default_kb_ru = ReplyKeyboardMarkup(
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

default_kb_kg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = 'Көз салуу'),
            KeyboardButton(text = 'Колдоо'),
        ],
        [
            KeyboardButton(text = 'Профиль'),
            KeyboardButton(text = 'Даректер'),
        ],
        [
            KeyboardButton(text = 'Көрсөтмөлөр'),
            KeyboardButton(text = 'Калькулятор'),
        ]
    ],
    resize_keyboard=True
)
cancel_calc_ru = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text = 'Отмена')
        ]
    ],
    resize_keyboard=True
)
cancel_calc_kg = ReplyKeyboardMarkup(
    keyboard= [
        [
            KeyboardButton(text = 'Артка')
        ]
    ],
    resize_keyboard=True
)


tracking_kb_ru = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'По трек-коду',callback_data = 'track-code')],
        [InlineKeyboardButton(text = 'По коду клиента',callback_data='client_id')]
    ]
)


tracking_kb_kg = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Трек код менен',callback_data = 'track-code')],
        [InlineKeyboardButton(text = 'Клиенттин коду менен',callback_data='client_id')]
    ]
)
