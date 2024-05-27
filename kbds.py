from aiogram.utils.keyboard import InlineKeyboardBuilder,InlineKeyboardMarkup
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

login_or_register_ru = ReplyKeyboardMarkup(
    keyboard= [
        [
        KeyboardButton(text = 'Войти'),
        KeyboardButton(text = 'Пройти регистрацию')
        ]
    ],
    resize_keyboard=True
)

login_or_register_kg = ReplyKeyboardMarkup(
    keyboard= [
        [
        KeyboardButton(text = 'Кируу'),
        KeyboardButton(text = 'Катталуу')
        ]
    ],
    resize_keyboard=True
)

set_city_kb = InlineKeyboardBuilder(
    markup= [
        [InlineKeyboardButton(text = 'Бишкек',callback_data='city_set_bish')],
        [InlineKeyboardButton(text = 'Ош',callback_data='city_set_osh')],
        [InlineKeyboardButton(text = 'Талас',callback_data='city_set_talas')],
        [InlineKeyboardButton(text = 'Жалал-Абад',callback_data='city_set_jl')],
        [InlineKeyboardButton(text = 'Узген',callback_data='city_set_uz')],
        [InlineKeyboardButton(text = 'Таш-Комур',callback_data='city_set_tash')],
        [InlineKeyboardButton(text = 'Ноокат',callback_data='city_set_nookat')],
        [InlineKeyboardButton(text = 'Баткен',callback_data='city_set_batken')],
        [InlineKeyboardButton(text = 'Екатеринбург',callback_data='city_set_eka')],
        [InlineKeyboardButton(text = 'Москва',callback_data='city_set_msk')],
        ]
)
profile_kb_ru = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Изменить профиль',callback_data='update_profile')],
        [get_lang_kb('RU')],
        [InlineKeyboardButton(text = 'Выйти из профиля',callback_data = 'logout_profile')]

    ]
)
profile_kb_kg = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Профилди өзгөртүү',callback_data='update_profile')],
        [get_lang_kb('KG')],
        [InlineKeyboardButton(text = 'Профилден чыгуу',callback_data = 'logout_profile')]
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
            KeyboardButton(text = '👤Профиль'),
            
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
        [InlineKeyboardButton(text = 'Жеке id боюнча',callback_data='client_id')]
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

set_variables_kbds = InlineKeyboardBuilder(
    markup = [
        [InlineKeyboardButton(text = 'Поменять цены',callback_data='set_prices')],
        [InlineKeyboardButton(text = 'Поменять ссылку для поддержки',callback_data = 're_whatsapp')],
        [InlineKeyboardButton(text = 'Поменять маркетплейсы',callback_data='set_marketplace')],
        [InlineKeyboardButton(text = 'Рассылка новостей',callback_data = 'send_broadcast')],
        [InlineKeyboardButton(text = 'Сменить пароль админа',callback_data = 'reset_password')],
        [InlineKeyboardButton(text = 'Сменить адрес Бишкек',callback_data = 'reset_city_bish')],
        [InlineKeyboardButton(text = 'Сменить адрес Ош',callback_data = 'reset_city_osh')],
        [InlineKeyboardButton(text = 'Сменить адрес Жалал-Абад',callback_data = 'reset_city_jl')],
        [InlineKeyboardButton(text = 'Сменить адрес Узген',callback_data = 'reset_city_uz')],
        [InlineKeyboardButton(text = 'Сменить адрес Таш-Комур',callback_data = 'reset_city_tash')],
        [InlineKeyboardButton(text = 'Сменить адрес Ноокат',callback_data = 'reset_city_nookat')],
        [InlineKeyboardButton(text = 'Сменить адрес Баткен',callback_data = 'reset_city_batken')],
        [InlineKeyboardButton(text = 'Сменить адрес Екатеринбург',callback_data = 'reset_city_eka')],
        [InlineKeyboardButton(text = 'Сменить адрес Москва',callback_data = 'reset_city_msk')],
        [InlineKeyboardButton(text = 'Сменить адрес Талас',callback_data = 'reset_city_talas')],
        [InlineKeyboardButton(text = 'Выйти',callback_data='logout_admin')]
    ]
)

set_marketplace = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Pinduoduo',callback_data = 'r_pinduoduo')],
        [InlineKeyboardButton(text = 'TAOBAO',callback_data = 'r_taobao')],
        [InlineKeyboardButton(text = '1688',callback_data = 'r_1688')],
        [InlineKeyboardButton(text = 'POIZON',callback_data = 'r_poizon')]
    ]
)

set_price = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = 'Цена по весу в Бишкеке',callback_data = 'p_price_weight_bish')],
        [InlineKeyboardButton(text = 'Цена по обьему в Бишкеке',callback_data = 'p_price_volume_bish')],
        [InlineKeyboardButton(text = 'Цена по весу в Оше',callback_data = 'p_price_weight_osh')],
        [InlineKeyboardButton(text = 'Цена по обьему в Оше',callback_data = 'p_price_volume_osh')],
        [InlineKeyboardButton(text = 'Цена по весу в Жалал-Абад',callback_data = 'p_price_weight_jl')],
        [InlineKeyboardButton(text = 'Цена по обьему в Жалал-Абад',callback_data = 'p_price_volume_jl')],
        [InlineKeyboardButton(text = 'Цена по весу в Талас',callback_data = 'p_price_weight_talas')],
        [InlineKeyboardButton(text = 'Цена по обьему в Талас',callback_data = 'p_price_volume_talas')],
        [InlineKeyboardButton(text = 'Цена по весу в Таш-Комур',callback_data = 'p_price_weight_tash')],
        [InlineKeyboardButton(text = 'Цена по обьему в Таш-Комур',callback_data = 'p_price_volume_tash')],
        [InlineKeyboardButton(text = 'Цена по весу в Ноокат',callback_data = 'p_price_weight_nookat')],
        [InlineKeyboardButton(text = 'Цена по обьему в Ноокат',callback_data = 'p_price_volume_nookat')],
        [InlineKeyboardButton(text = 'Цена по весу в Баткен',callback_data = 'p_price_weight_batken')],
        [InlineKeyboardButton(text = 'Цена по обьему в Баткен',callback_data = 'p_price_volume_batken')],
        [InlineKeyboardButton(text = 'Цена по весу в Узген',callback_data = 'p_price_weight_uz')],
        [InlineKeyboardButton(text = 'Цена по обьему в Узген',callback_data = 'p_price_volume_uz')],
        [InlineKeyboardButton(text = 'Цена по весу в Екатеринберг',callback_data = 'p_price_weight_eka')],
        [InlineKeyboardButton(text = 'Цена по обьему в Екатеринберг',callback_data = 'p_price_volume_eka')],
        [InlineKeyboardButton(text = 'Цена по весу в Москва',callback_data = 'p_price_weight_msk')],
        [InlineKeyboardButton(text = 'Цена по обьему в Москва',callback_data = 'p_price_volume_msk')],
    ]
)
        