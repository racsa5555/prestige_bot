from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton,ReplyKeyboardMarkup,KeyboardButton

def get_lang_kb(current_lang):
    if current_lang == 'RU':
        flag = '🇰🇬'
        new_lang = 'KG'
    else:
        flag = '🇷🇺'
        new_lang = 'RU'
    kb = InlineKeyboardButton(text = f'Переключить язык на {flag}',callback_data = f'switch_language_{new_lang}')
    return kb

set_city_kb = InlineKeyboardBuilder(
    markup= [
        [InlineKeyboardButton(text = 'Бишкек',callback_data='city_set_bishkek'),
        InlineKeyboardButton(text = 'Каракол',callback_data='city_set_kk')]
    ]   
)   
profile_kb_ru = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Изменить профиль',callback_data='update_profile')],
        [get_lang_kb('RU')]
    ]
)
profile_kb_kg = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Профилди өзгөртүү',callback_data='update_profile')],
        [get_lang_kb('KG')]
    ]
)

default_kb_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = '🔎Отслеживание'),
            KeyboardButton(text = '👤Профиль'),
            
        ],
        [
            KeyboardButton(text = '⚙️Поддержка'),
            KeyboardButton(text = '📬Адреса'),
        ],
        [
            KeyboardButton(text = '📏Калькулятор'),
            KeyboardButton(text = '📕Инструкция'),
        ]
    ],
    resize_keyboard=True
)

default_kb_kg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = '🔎Издөө'),
            KeyboardButton(text = '👤Кароо'),
            
        ],
        [
            KeyboardButton(text = '⚙️Колдоо'),
            KeyboardButton(text = '📬Дарек'),
        ],
        [
            KeyboardButton(text = '📏Эсептөөчү'),
            KeyboardButton(text = '📕Нускама'),
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
        [InlineKeyboardButton(text = 'Трек код боюнча',callback_data = 'track-code')],
        [InlineKeyboardButton(text = 'Жеке жактар боюнча id',callback_data='client_id')]
    ]
)

instruction_kb = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Pinduoduo',callback_data = 'choose_pin')],
        [InlineKeyboardButton(text = 'Taobao',callback_data = 'choose_tao')],
        [InlineKeyboardButton(text = '1688',callback_data = 'choose_1688')],
        [InlineKeyboardButton(text = 'Poizon',callback_data = 'choose_poi')]
    ]
)

