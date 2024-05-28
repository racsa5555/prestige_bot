import asyncio 

import pandas as pd
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart,Command
from aiogram import F

from decouple import config

from aiogram.fsm.context import FSMContext

from goole_sheet import register_client,find_order_by_id,update_google_sheet,find_order_by_track_code,update_client_by_id,append_products,find_user_by_data
from states import UserState,Calculator,Admin,Track_code,RegisterState
from kbds import *
from variables import *

LIST_USERS = set()



TOKEN = config('TOKEN')

bot = Bot(TOKEN)

dp = Dispatcher()

id = 2000

@dp.message(CommandStart())
async def start(message: types.Message,state:FSMContext):
    language_kb = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = '🇷🇺',callback_data='lang_RU'),
        InlineKeyboardButton(text = '🇰🇬',callback_data='lang_KG')]
    ])
    ref = message.text.split()
    if len(ref) == 2:
        if ref == 'wsayMHwjKHdY':
            await state.update_data(ref = ref)
    await message.answer("Выберите язык / Тилди тандаңыз:", reply_markup=language_kb.as_markup())


@dp.callback_query(lambda query: query.data.startswith('lang_'))
async def set_lang(callback:CallbackQuery,state:FSMContext):
    await state.update_data(language=callback.data[-2:])
    data = await state.get_data()
    if not (data.get('id') == None):
        if data['language'] == 'RU':
            await callback.message.answer(text = 'Вы сменили язык на Русский',reply_markup = default_kb_ru)
        else:
            await callback.message.answer(text = 'Сиз тилди Кыргызчага алмаштырдыңыз',reply_markup = default_kb_kg)
    else:
        await hi(callback.message,state)


@dp.callback_query(lambda query: query.data.startswith('switch_language_'))
async def set_l(callback:CallbackQuery,state:FSMContext):
    await set_lang(callback,state)



@dp.callback_query(lambda query: query.data == 'update_profile')
async def set_bish(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    await state.update_data(update = True)
    if data['language'] == 'RU':
        await callback.message.answer(text = 'С какого Вы города?',reply_markup=set_city_kb.as_markup())
    else:
        await callback.message.answer(text = 'Кайсыл шаардан болосуз?',reply_markup=set_city_kb.as_markup())


@dp.message(UserState.hi)
async def hi(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    if data['language'] == 'RU':
        data.pop('language')
        if not data or len(data) == 1:
            await message.answer(text = 'Здравствуйте 👋\nПеред использованием бота нужно пройти регистрацию или войти',reply_markup = login_or_register_ru)
        else:
            await message.answer(text = 'Вы уже вошли в аккаунт')
    else:
        data.pop('language')
        if not data or len(data) == 1:
            await message.answer(text = 'Саламатсызбы\nБотту иштетүүгө чейин сөссүз катталып алышыңыз керек же кирүү',reply_markup = login_or_register_kg)
        else:
            await message.answer(text = 'Сиз уже катталгынсыз')


@dp.message(F.text.in_({'Пройти регистрацию','Катталуу'}))
async def register(message:Message,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        await message.answer(text = 'С какого Вы города',reply_markup=set_city_kb.as_markup())
    else:
        await message.answer(text = 'Кайсыл шаардан болосуз?',reply_markup=set_city_kb.as_markup())


@dp.message(F.text.in_({'Войти','Кируу'}))
async def login(message:Message, state: FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        await message.answer(text = 'Введите номер телефона',reply_markup=cancel_calc_ru)
    else:
        await message.answer(text = 'Телефон номериңизди жазыныз',reply_markup=cancel_calc_kg)
    await state.set_state(RegisterState.phone_number)

@dp.message(RegisterState.phone_number)
async def set_ph_n(message:Message,state:FSMContext):
    if message.text == 'Отмена' or message.text == 'Артка':
        await hi(message,state)
        return
    data = await state.get_data()
    await state.update_data(phone_number = message.text)
    if data['language'] == 'RU':
        text = 'Введите персональный код'
        mark = cancel_calc_ru
    else:
        text = 'Жеке код жазыныз'
        mark = cancel_calc_kg
    await message.answer(text = text,reply_markup=mark)
    await state.set_state(RegisterState.client_id)

@dp.message(RegisterState.client_id)
async def set_id(message:Message,state:FSMContext):
    if message.text == 'Отмена' or message.text == 'Артка':
        await hi(message,state)
        return
    else:
        data = await state.get_data()
        phone_number = data.get('phone_number')
        client_id = message.text
        if data.get('language') == 'RU':
            await message.answer(text = 'Обработка, подождите несколько секунд...')
        else:
            await message.answer(text = 'Күтүп турунуз...')
        res = find_user_by_data(phone_number,client_id,data['language'])
        if type(res) == dict:
            await state.set_data(res)
            await message.answer(text = send_profile(res),reply_markup=default_kb_ru)
            await state.set_state()
        else:
            await message.answer(text = res)

@dp.callback_query(lambda query: query.data.startswith('city_set'))
async def set_bish(callback:CallbackQuery,state:FSMContext):
    if callback.data == 'city_set_bish':
        await state.update_data(city = 'BISH')
    elif callback.data == 'city_set_jl':
        await state.update_data(city = 'JL')
    elif callback.data == 'city_set_osh':
        await state.update_data(city = 'OSH')
    elif callback.data == 'city_set_talas':
        await state.update_data(city = 'TA')
    elif callback.data == 'city_set_batken':
        await state.update_data(city = 'BAT')
    elif callback.data == 'city_set_uz':
        await state.update_data(city = 'UZ')
    elif callback.data == 'city_set_nookat':
        await state.update_data(city = 'N')
    elif callback.data == 'city_set_msk':
        await state.update_data(city = 'MOS')
    elif callback.data == 'city_set_eka':
        await state.update_data(city = 'EKA')
    elif callback.data == 'city_set_tash':
        await state.update_data(city = 'TASH')


    data = await state.get_data()
    if data['language'] == 'RU':
        await callback.message.answer(text = 'Как Вас зовут?')
    else:
        await callback.message.answer(text = 'Сиздин атыңыз ким?')
    await state.set_state(UserState.name)

@dp.message(UserState.name)
async def set_name(message:Message,state:FSMContext):
    data = await state.get_data()
    if len(message.text.split()) == 1:
        await state.update_data(name = message.text)
        await state.set_state(UserState.full_name)
        if data['language'] == 'RU':
            await message.answer(text = 'Как Ваша фамилия?')
        else:
            await message.answer(text = 'Сиздин фамилияңыз кандай?')
    else:
        if data['language'] == 'RU':
            await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')
        else:
            await message.answer('❗️ Туура эмес формат ❗️\nКайра жазып көрүнүз')


@dp.message(UserState.full_name)
async def set_full_name(message:Message,state:FSMContext):
    mas = message.text.split()
    fullname = ''.join(mas)
    await state.update_data(full_name = fullname)
    await state.set_state(UserState.phone_number)
    data = await state.get_data()
    if data['language'] == 'RU':
        await message.answer(text = 'Пожалуйста, напишите номер телефона,\nпример: 0708999963')
    else:
        await message.answer(text = 'Сураныч , телефон номеринизди жазыныз, \n мисалы: 0708999963')


@dp.message(UserState.phone_number)
async def set_phone_number(message:Message,state:FSMContext):
    if message.text.isdigit():
        await state.update_data(phone_number = message.text)
        data = await state.get_data()
        update =  data.get('update')
        if update == True:
            fio = data.get('full_name') +' ' + data.get('name')
            data_new = {'Город':data.get('city'),
                        'ФИО':fio,
                        'Номер':data.get('phone_number')}
            if data['language'] == 'RU':
                default_kb = default_kb_ru
                profile_kb = profile_kb_ru
                await message.answer(text = '✅ Успешное обновление профиля !',reply_markup=default_kb)
                await message.answer(text = send_profile(data),reply_markup=profile_kb.as_markup())
            else:
                default_kb = default_kb_kg
                profile_kb = profile_kb_kg
                await message.answer(text = '✅ Ийгиликтүү профильди өзгөртүп алдыныз !',reply_markup=default_kb)
                await message.answer(text = send_profile(data),reply_markup=profile_kb.as_markup())
            update_client_by_id(data.get('id'),data_new,data.get('ref'))
            await state.set_state()
        else:
            global id
            await state.update_data(id = id)
            id+=1
            data = await state.get_data()
            if data['language'] == 'RU':
                default_kb = default_kb_ru
                profile_kb = profile_kb_ru
                global LIST_USERS
                LIST_USERS.add(message.from_user.id)
                await message.answer(text = '✅ Успешная регистрация !',reply_markup=default_kb)
                await message.answer(text = send_profile(data),reply_markup=profile_kb.as_markup())
            else:
                default_kb = default_kb_kg
                profile_kb = profile_kb_kg
                LIST_USERS.add(message.from_user.id)
                await message.answer(text = '✅ Ийгиликтүү каттоо !',reply_markup=default_kb)
                await message.answer(text = send_profile(data),reply_markup=profile_kb.as_markup())
            register_client(data)
            await state.set_state()
    else:
        data = await state.get_data()
        if data['language'] == 'RU':
            await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')
        else:
            await message.answer('❗️ Туура эмес формат ❗️\nКайра жазып көрүнүз')

@dp.message(F.text[1:].in_({'Профиль','Кароо'}))
async def get_profile(message:Message,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        res = send_profile(data)
        profile_kb = profile_kb_ru
        await message.answer(text = res,reply_markup=profile_kb.as_markup())
    else:
        profile_kb = profile_kb_kg
        res = send_profile(data)
        await message.answer(text = res,reply_markup=profile_kb.as_markup())

@dp.message(F.text[1:].in_({'Адреса','Дарек'}))
async def get_address(message:Message,state:FSMContext):
    global ADRESS_BISH
    global ADRESS_OSH
    global ADRESS_SOKULUK
    global ADRESS_TOKMOK
    global ADRESS_GULCHO
    data = await state.get_data()
    lang = data.get('language')
    res = str(send_adress(data.get('id'),data.get('phone_number'),lang,data.get('city'),ADRESS_BISH,ADRESS_OSH,ADRESS_TOKMOK,ADRESS_SOKULUK,ADRESS_GULCHO))
    await message.answer(text = res)


@dp.message(F.text[1:].in_({'Калькулятор','Эсептөөчү'}))
async def set_start(message:Message,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        cancel_calc = cancel_calc_ru
        await message.answer(text = 'Введите длину (см)',reply_markup=cancel_calc)
    else:
        cancel_calc = cancel_calc_kg
        await message.answer(text = 'Узундугун жазыныз (см)',reply_markup=cancel_calc) 
    await state.set_state(Calculator.length)

@dp.message(Calculator.length)
async def set_length(message:Message,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        if message.text.isdigit():
            cancel_calc = cancel_calc_ru
            default_kb = default_kb_ru
            await state.update_data(length = int(message.text))
            await message.answer(text = 'Введите ширину (см)',reply_markup=cancel_calc)
            await state.set_state(Calculator.width)
        elif message.text == 'Отмена':
            default_kb = default_kb_ru
            await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
            await state.set_state()
        else:
            await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')
    else:
        if message.text.isdigit():
            cancel_calc = cancel_calc_kg
            default_kb = default_kb_kg
            await state.update_data(length = int(message.text))
            await message.answer(text = 'Туурасын жазыныз (см)',reply_markup=cancel_calc)
            await state.set_state(Calculator.width)
        elif message.text == 'Артка':
            default_kb = default_kb_kg
            await message.answer(text = 'Акыркы аракетиңизди артка кайтардыңыз',reply_markup=default_kb)
            await state.set_state()
        else:
            await message.answer('❗️ Туура эмес формат ❗️\nКайра жазып көрүнүз')

@dp.message(Calculator.width)
async def set_width(message:Message,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        default_kb = default_kb_ru
        if message.text.isdigit():
            cancel_calc = cancel_calc_ru
            await state.update_data(width = int(message.text))
            await message.answer(text = 'Введите высоту (см)',reply_markup=cancel_calc)
            await state.set_state(Calculator.height)
        elif message.text == 'Отмена':
            await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
            await state.set_state()
        else:
            await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')
    else:
        default_kb = default_kb_kg
        if message.text.isdigit():
            cancel_calc = cancel_calc_kg
            await state.update_data(width = int(message.text))
            await message.answer(text = 'Бийиктигин жазыныз (см)',reply_markup=cancel_calc)
            await state.set_state(Calculator.height)
        elif message.text == 'Артка':
            await message.answer(text = 'Акыркы аракетиңизди артка кайтардыңыз',reply_markup=default_kb)
            await state.set_state()
        else:
            await message.answer('❗️ Туура эмес формат ❗️\nКайра жазып көрүнүз')

@dp.message(Calculator.height)
async def set_height(message:Message,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        default_kb = default_kb_ru
        if message.text.isdigit():
            cancel_calc = cancel_calc_ru
            await state.update_data(height = int(message.text))
            await message.answer(text = 'Введите вес (кг)',reply_markup=cancel_calc)
            await state.set_state(Calculator.weight)
        elif message.text == 'Отмена':
            await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
            await state.set_state()
        else:
            await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')
    else:
        default_kb = default_kb_kg
        if message.text.isdigit():
            cancel_calc = cancel_calc_kg
            await state.update_data(height = int(message.text))
            await message.answer(text = 'Салмагын жазыныз (кг)',reply_markup=cancel_calc)
            await state.set_state(Calculator.weight)
        elif message.text == 'Артка':
            await message.answer(text = 'Акыркы аракетиңизди артка кайтардыңыз',reply_markup=default_kb)
            await state.set_state()
        else:
            await message.answer('❗️ Туура эмес формат ❗️\nКайра жазып көрүнүз')

@dp.message(F.text[1:].in_({'Артка','Отмена'}))
async def cancel(message:Message,state:FSMContext):
    data = await state.get_data()
    default_kb = None
    if data['language'] == 'RU':
        default_kb = default_kb_ru
        await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
    else:
        default_kb = default_kb_kg
        await message.answer(text = 'Акыркы аракетиңизди артка кайтардыңыз',reply_markup=default_kb)
    await state.set_state()


@dp.message(Calculator.weight)
async def set_width(message:Message,state:FSMContext):
    if message.text.isdigit():
        await state.update_data(weight = int(message.text))
        data = await state.get_data()
        if data.get('city') == 'BISH':
            global PRICE_VOLUME_BISH
            global PRICE_WEIGHT_BISH
            price_weight = PRICE_WEIGHT_BISH
            price_volume = PRICE_VOLUME_BISH
        elif data.get('city') == 'OSH':
            global PRICE_VOLUME_OSH
            global PRICE_WEIGHT_OSH
            price_weight = PRICE_WEIGHT_OSH
            price_volume = PRICE_VOLUME_OSH
        elif data.get('city') == 'JL':
            global PRICE_VOLUME_JL
            global PRICE_WEIGHT_JL
            price_weight = PRICE_WEIGHT_JL
            price_volume = PRICE_VOLUME_JL
        elif data.get('city') == 'TA':
            global PRICE_VOLUME_TALAS
            global PRICE_WEIGHT_TALAS
            price_weight = PRICE_WEIGHT_TALAS
            price_volume = PRICE_VOLUME_TALAS
        elif data.get('city') == 'UZ':
            global PRICE_VOLUME_UZ
            global PRICE_WEIGHT_UZ
            price_weight = PRICE_WEIGHT_UZ
            price_volume = PRICE_VOLUME_UZ
        elif data.get('city') == 'TASH':
            global PRICE_VOLUME_TASH
            global PRICE_WEIGHT_TASH
            price_weight = PRICE_WEIGHT_TASH
            price_volume = PRICE_VOLUME_TASH
        elif data.get('city') == 'BAT':
            global PRICE_VOLUME_BATKEN
            global PRICE_WEIGHT_BATKEN
            price_weight = PRICE_WEIGHT_BATKEN
            price_volume = PRICE_VOLUME_BATKEN
        elif data.get('city') == 'EKA':
            global PRICE_VOLUME_EKA
            global PRICE_WEIGHT_EKA
            price_weight = PRICE_WEIGHT_EKA
            price_volume = PRICE_VOLUME_EKA
        elif data.get('city') == 'MOS':
            global PRICE_VOLUME_MSK
            global PRICE_WEIGHT_MSK
            price_weight = PRICE_WEIGHT_MSK
            price_volume = PRICE_VOLUME_MSK
            
        volume_price = (data['width'] * data['height'] * data ['length'])/1000000 * price_volume
        weight_price = data['weight'] * price_weight
        max_price = round(max(volume_price,weight_price),1)
        data = await state.get_data()
        if data['language'] == 'RU':
            default_kb = default_kb_ru
            await message.answer(text = f'Ваша цена: {max_price} $',reply_markup=default_kb)
        else:
            default_kb = default_kb_kg
            await message.answer(text = f'Сиздин бааңыз: {max_price} $',reply_markup=default_kb)
        await state.set_state()
    elif message.text == 'Отмена':
        default_kb = default_kb_ru
        await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
        await state.set_state()
    elif message.text == 'Артка':
        default_kb = default_kb_kg
        await message.answer(text = 'Акыркы аракетиңизди артка кайтардыңыз',reply_markup=default_kb)
        await state.set_state()
    else:
        await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')



@dp.message(F.text[1:].in_({'Издөө','Отслеживание'}))
async def tracking(message:Message,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        tracking_kb = tracking_kb_ru
        await message.answer(text = 'Выберите способ отслеживания',reply_markup=tracking_kb.as_markup())
    else:
        tracking_kb = tracking_kb_kg
        await message.answer(text = 'Издөө режим тандаңыз',reply_markup=tracking_kb.as_markup())


@dp.callback_query(lambda query: query.data == 'client_id')
async def tracking_by_client_id(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    client_id = data.get('id')
    lang = data.get('language')
    if data.get('language') == 'RU':
        await callback.message.answer(text = 'Обработка, подождите несколько секунд...')
    else:
        await callback.message.answer(text = 'Күтүп турунуз...')
    res = find_order_by_id(str(client_id),lang)
    await callback.message.answer(text = res)


@dp.callback_query(lambda query: query.data == 'track-code')
async def tracking_by_client_id(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        await callback.message.answer(text = 'Введите трек-код товара',reply_markup=cancel_calc_ru)
    else:
        await callback.message.answer(text ='Товардын трек кодун жазыңыз',reply_markup = cancel_calc_kg)
    await state.set_state(Track_code.track_code)


@dp.message(Track_code.track_code)
async def track_code(message:Message,state:FSMContext):
    track_code = message.text
    if message.text in {'Отмена','Артка'}:
        data = await state.get_data()
        lang = data.get('language')
        res = cancel_sender(lang)
        if lang == 'RU':
            default_kb = default_kb_ru
        else:
            default_kb = default_kb_kg
        await message.answer(text = res,reply_markup=default_kb)
        await state.set_state()
    else: 
        data = await state.get_data()
        if data.get('language') == 'RU':
            await message.answer(text = 'Обработка, подождите несколько секунд...')
        else:
            await message.answer(text = 'Күтүп турунуз...')
        res = find_order_by_track_code(track_code,data.get('language'))
        await message.answer(text = res)


@dp.message(Command(commands=['admin']))
async def admin_mode(message:Message,state:FSMContext):
    await message.answer(text = 'Введите пароль')
    await state.set_state(Admin.password)

@dp.message(Admin.password)
async def get_password(message:Message,state:FSMContext):
    if message.text == ADMIN_PASSWORD:
        await message.answer(text = 'Вы успешно вошли в режим админа\n Отправьте excel таблицу с трек кодами и с текстом статуса',reply_markup=set_variables_kbds.as_markup())
        await state.update_data(is_admin = True)
        await state.set_state()
    else:
        await message.answer(text = 'Неверный пароль,попробуйте еще раз')


@dp.callback_query(lambda query: query.data.startswith('set_'))
async def set_variables(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    if data.get('is_admin') == True:
        if callback.data == 'set_marketplace':
            await callback.message.answer(text = 'Выберите у какого маркетплейса хотите поменять ссылку/текст',reply_markup=set_marketplace.as_markup())
        if callback.data == 'set_prices':
            await callback.message.answer(text = 'Выберите у какой переменной хотите поменять значение',reply_markup=set_price.as_markup())
    else:
        await callback.message.answer(text = 'У вас нет прав')


@dp.callback_query(lambda query: query.data.startswith('r_'))
async def set_market(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    if data.get('is_admin') == True:
        await state.update_data(data = {'data':callback.data[2:]})
        await callback.message.answer(text = f'Введите новую ссылку для маркетплейса {callback.data[2:]}')
        await state.set_state(Admin.set_price)
    else:
        await callback.message.answer(text = 'У вас нет прав')


@dp.callback_query(lambda query: query.data.startswith('reset_city_'))
async def reset_city(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    if data.get('is_admin') == True:
        await callback.message.answer(text = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000')
        await state.update_data(data = {'data':callback.data[11:]})
        await state.set_state(Admin.set_price)
    else:
        await callback.message.answer(text = 'У вас нет прав')

@dp.callback_query(lambda query: query.data == 'reset_password')
async def reset_password(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    if data.get('is_admin') == True:
        await callback.message.answer(text = 'Введите новый пароль')
        await state.update_data(data = {'data':'resetpassword'})
        await state.set_state(Admin.set_price)
    else:
        await callback.message.answer(text = 'У вас нет прав')


@dp.callback_query(lambda query: query.data == 're_whatsapp')
async def re_whatsapp(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    if data.get('is_admin') == True:
        await callback.message.answer(text = 'Введите новую ссылку для Whatsapp')
        await state.update_data(data = {'data':'whatsapp'})
        await state.set_state(Admin.set_price)
    else:
        await callback.message.answer(text = 'У вас нет прав')

@dp.callback_query(lambda query: query.data.startswith('p_'))
async def set_price_v(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    if data.get('is_admin') == True:
        await state.update_data(data = {'data':callback.data[8:]})
        await callback.message.answer(text = 'Введите новое значение')
        await state.set_state(Admin.set_price)
    else:
        await callback.message.answer(text = 'У вас нет прав')


@dp.callback_query(lambda query: query.data == 'send_broadcast')
async def send_b(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    if data.get('is_admin') == True:
        await callback.message.answer(text = 'Введите новость')
        await state.set_state(Admin.news)
    else:
        await callback.message.answer(text = 'У вас нет прав')


@dp.message(Admin.news)
async def send_new(message:Message,state:FSMContext):
    data = await state.get_data()
    if data.get('is_admin') == True:
        text = message.text
        await send_news(text)
        await message.answer(text = 'Новость успешно разослана')
        await state.set_state()
    else:
        await message.answer(text = 'У вас нет прав')


@dp.message(Admin.set_price)
async def set_price_v2(message:Message,state:FSMContext):
    data = await state.get_data()
    if data.get('is_admin') == True:
        new_value = message.text    
        global PRICE_VOLUME_BISH
        global PRICE_WEIGHT_BISH
        global PRICE_VOLUME_OSH
        global PRICE_WEIGHT_OSH
        global PRICE_VOLUME_TALAS
        global PRICE_WEIGHT_TALAS
        global PRICE_VOLUME_BATKEN
        global PRICE_WEIGHT_BATKEN
        global PRICE_VOLUME_TASH
        global PRICE_WEIGHT_TASH
        global PRICE_VOLUME_UZ
        global PRICE_WEIGHT_UZ
        global PRICE_VOLUME_JL
        global PRICE_WEIGHT_JL
        global PRICE_VOLUME_NOOKAT
        global PRICE_WEIGHT_NOOKAT
        global PRICE_VOLUME_EKA
        global PRICE_WEIGHT_EKA
        global PRICE_VOLUME_MSK
        global PRICE_WEIGHT_MSK
        global TAOBAO
        global ONE_AND_SIX
        global PINDUODUO
        global POIZON
        global LINK_WHATSAPP
        global ADMIN_PASSWORD
        global ADRESS_BISH
        global ADRESS_OSH
        global ADRESS_TASH
        global ADRESS_TALAS
        global ADRESS_UZ
        global ADRESS_JL
        global ADRESS_BATKEN
        global ADRESS_NOOKAT
        global ADRESS_EKA
        global ADRESS_MSK
        if '_' in data['data']:
            if data['data'] == 'volume_bish':
                PRICE_VOLUME_BISH = float(new_value)
            elif data['data'] == 'weight_bish':
                PRICE_WEIGHT_BISH = float(new_value)
            if data['data'] == 'volume_osh':
                PRICE_VOLUME_OSH = float(new_value)
            elif data['data'] == 'weight_osh':
                PRICE_WEIGHT_OSH = float(new_value)
            if data['data'] == 'volume_tash':
                PRICE_VOLUME_TASH = float(new_value)
            elif data['data'] == 'weight_tash':
                PRICE_WEIGHT_TASH = float(new_value)
            if data['data'] == 'volume_uz':
                PRICE_VOLUME_UZ = float(new_value)
            elif data['data'] == 'weight_uz':
                PRICE_WEIGHT_UZ = float(new_value)
            if data['data'] == 'volume_jl':
                PRICE_VOLUME_JL = float(new_value)
            elif data['data'] == 'weight_jl':
                PRICE_WEIGHT_JL = float(new_value)
            if data['data'] == 'volume_nookat':
                PRICE_VOLUME_NOOKAT = float(new_value)
            elif data['data'] == 'weight_nookat':
                PRICE_WEIGHT_NOOKAT = float(new_value)
            if data['data'] == 'volume_batken':
                PRICE_VOLUME_BATKEN = float(new_value)
            elif data['data'] == 'weight_batken':
                PRICE_WEIGHT_BATKEN = float(new_value)
            if data['data'] == 'volume_talas':
                PRICE_VOLUME_TALAS = float(new_value)
            elif data['data'] == 'weight_talas':
                PRICE_WEIGHT_TALAS = float(new_value)
            if data['data'] == 'volume_msk':
                PRICE_VOLUME_MSK = float(new_value)
            elif data['data'] == 'weight_msk':
                PRICE_WEIGHT_MSK = float(new_value)
            if data['data'] == 'volume_eka':
                PRICE_VOLUME_EKA = float(new_value)
            elif data['data'] == 'weight_eka':
                PRICE_WEIGHT_EKA = float(new_value)
            await message.answer(text = 'Вы успешно сменили цену')
        elif data['data'] == 'whatsapp':
            LINK_WHATSAPP = new_value
            await message.answer(text = 'Вы успешно сменили ссылку на whatsapp')
        elif data['data'] == 'resetpassword':
            ADMIN_PASSWORD = new_value
            await message.answer(text = 'Вы сменили пароль')
        if data['data'] == 'bish':
            ADRESS_BISH = str(new_value)
            await message.answer(text = 'Вы сменили адрес Бишкека')
        elif data['data'] == 'osh':
            ADRESS_OSH = str(new_value)
            await message.answer(text = 'Вы сменили адрес Оша')
        elif data['data'] == 'talas':
            ADRESS_TALAS = str(new_value)
            await message.answer(text = 'Вы сменили адрес Таласа')
        elif data['data'] == 'nookat':
            ADRESS_NOOKAT = str(new_value)
            await message.answer(text = 'Вы сменили адрес Ноокат')
        elif data['data'] == 'jl':
            ADRESS_JL = str(new_value)
            await message.answer(text = 'Вы сменили адрес Жалал-Абад')
        elif data['data'] == 'tash':
            ADRESS_TASH = str(new_value)
            await message.answer(text = 'Вы сменили адрес Таш-Комур')
        elif data['data'] == 'batken':
            ADRESS_BATKEN = str(new_value)
            await message.answer(text = 'Вы сменили адрес Баткен')
        elif data['data'] == 'uz':
            ADRESS_UZ = str(new_value)
            await message.answer(text = 'Вы сменили адрес Узгена')
        elif data['data'] == 'msk':
            ADRESS_MSK = str(new_value)
            await message.answer(text = 'Вы сменили адрес Москвы')
        elif data['data'] == 'eka':
            ADRESS_EKA = str(new_value)
            await message.answer(text = 'Вы сменили адрес Екатеринбурга')
        else:
            if data['data'] == 'taobao':
                TAOBAO = new_value
            elif data['data'] == 'pinduoduo':
                PINDUODUO = new_value
            elif data['data'] == 'poizon':
                POIZON = new_value
            elif data['data'] == '1688':
                ONE_AND_SIX = new_value        
            await message.answer(text = 'Вы успешно сменили ссылку')
        await state.set_state()
    else:
        await message.answer(text = 'У вас нет прав')



@dp.message(F.document)
async def handle_admin_documents(message: types.Message, state: FSMContext):
    data = await state.get_data()
    statuses = {'В Китае','В Пути','В КР'}
    if data.get("is_admin") == True:
        if message.caption not in statuses:
            await message.answer(text = f'Введите к прикрепленному файлу один из статусов:{statuses}')
        else:
            file_info = await bot.get_file(message.document.file_id)
            file_path = file_info.file_path
            file = await bot.download_file(file_path)
            df = pd.read_excel(file,header = None)
            track_codes = df.iloc[:,0].to_list()
            if len(df.columns) == 3:
                w = True
                data = df.iloc[:, :3]
            else:
                w = False
                data = df.iloc[:, :2]
            new_status = message.caption
            if new_status == 'В Китае':
                append_products(data,w)
                await message.answer('Все готово,проверьте')
            else:
                update_google_sheet(set(track_codes),new_status)
                await message.answer('Все готово,проверьте')
    else:
        await message.answer('Неверный формат ввода')


@dp.message(F.text[2:].in_({'Поддержка','Колдоо'}))
async def help(message:Message,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        await message.answer(text = f'🛠️Контакт для поддержки📩\n{LINK_WHATSAPP}')
    else:
        await message.answer(text = f'🛠️Колдоо байланыш📩\n{LINK_WHATSAPP}')


@dp.message(F.text[1:].in_({'Инструкция','Нускама'}))
async def send_video(message:Message,state:FSMContext):
    data = await state.get_data()
    if data.get('language') == 'RU': 
        await message.answer(text = 'Выберите маркетплейс',reply_markup=instruction_kb.as_markup())
    else:
        await message.answer(text = 'Сайт тандаңыз',reply_markup=instruction_kb.as_markup())


@dp.callback_query(lambda query: query.data.startswith('choose_'))
async def instruction(callback:CallbackQuery):
    data = callback.data[7:]
    if data == 'pin':
        await callback.message.answer(text = PINDUODUO)
    elif data == 'tao':
        await callback.message.answer(text = TAOBAO)
    elif data == '1688':
        await callback.message.answer(text = ONE_AND_SIX)
    elif data == 'poi':
        await callback.message.answer(text = POIZON)

async def send_news(message):
    global LIST_USERS
    for user_id in LIST_USERS:
        await bot.send_message(user_id,message)


@dp.callback_query(lambda query: query.data == 'logout_admin')
async def logout_admin(callback:CallbackQuery,state:FSMContext):
    await state.clear()
    await callback.message.answer(text = 'Вы вышли из режима администратора')
    await state.set_state()

@dp.callback_query(lambda query: query.data == 'logout_profile')
async def logout_profile(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    if data['language'] == 'RU':
        await callback.message.answer(text = 'Вы вышли из профиля')
    else:
        await callback.message.answer(text = 'Профилден чыктыныз')
    await state.clear()
    await state.update_data({'language':data['language']})
    await hi(callback.message,state)


async def main():
    await dp.start_polling(bot)



asyncio.run(main())