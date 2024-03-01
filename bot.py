import asyncio 
from typing import Any, Dict

import pandas as pd
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart,Command
from aiogram import F


from decouple import config

from aiogram.fsm.context import FSMContext

from goole_sheet import register_client,find_order_by_id,update_google_sheet,find_order_by_track_code,update_client_by_id,append_products
from states import UserState,Calculator,Admin,Track_code
from kbds import *
from variables import *

LIST_USERS = set()



TOKEN = config('TOKEN')

bot = Bot(TOKEN)

dp = Dispatcher()

id = 2104

@dp.message(CommandStart())
async def start(message: types.Message):
    language_kb = InlineKeyboardBuilder(
    markup=[
        [InlineKeyboardButton(text = '🇷🇺',callback_data='lang_RU'),
        InlineKeyboardButton(text = '🇰🇬',callback_data='lang_KG')]
    ])
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
        if not data:
            await message.answer(text = 'Здравствуйте 👋\nПеред использованием бота нужно пройти регистрацию 😎')
            await message.answer(text = 'С какого Вы города',reply_markup=set_city_kb.as_markup())
        else:
            await message.answer(text = 'Вы уже вошли в аккаунт')
    else:
        data.pop('language')
        if not data:
            await message.answer(text = 'Саламатсызбы \n ботту иштеткен ге чейин сөссүз катталып алышыңыз керек 😎')
            await message.answer(text = 'Кайсыл шаардан болосуз?',reply_markup=set_city_kb.as_markup())
        else:
            await message.answer(text = 'Сиз уже катталгынсыз')

@dp.callback_query(lambda query: query.data.startswith('city_set'))
async def set_bish(callback:CallbackQuery,state:FSMContext):
    if callback.data == 'city_set_kk':
        await state.update_data(city = 'KK')
    else:
        await state.update_data(city = 'BISH')
    data = await state.get_data()
    if data['language'] == 'RU':
        await callback.message.answer(text = 'Как Вас зовут?')
    else:
        await callback.message.answer(text = 'Сиздин атыңыз ким?')
    await state.set_state(UserState.name)

@dp.message(UserState.name)
async def set_name(message:Message,state:FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(UserState.full_name)
    data = await state.get_data()
    if data['language'] == 'RU':
        await message.answer(text = 'Как Ваша фамилия?')
    else:
        await message.answer(text = 'Сиздин фамилияңыз кандай?')


@dp.message(UserState.full_name)
async def set_full_name(message:Message,state:FSMContext):
    await state.update_data(full_name = message.text)
    await state.set_state(UserState.phone_number)
    data = await state.get_data()
    if data['language'] == 'RU':
        await message.answer(text = 'Пожалуйста, напишите номер телефона,\nпример: 996ХХХХХХХХХ')
    else:
        await message.answer(text = 'Сураныч , телефон номеринизди жазыныз, \n мисалы: 996ХХХХХХХХХ')

@dp.message(UserState.phone_number)
async def set_phone_number(message:Message,state:FSMContext):
    if message.text.isdigit():
        await state.update_data(phone_number = message.text)
        data = await state.get_data()
        update =  data.get('update')
        if update == True:
            fio = data.get('full_name') + data.get('name')
            data_new = {'Город':data.get('city'),
                        'ФИО':fio,
                        'Номер':data.get('phone_number')}
            update_client_by_id(data.get('id'),data_new)
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
    data = await state.get_data()
    lang = data.get('language')
    res = send_adress(data.get('id'),data.get('phone_number'),lang)
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
            await message.answer(text = 'Узундугун жазыныз (см)',reply_markup=cancel_calc)
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
            await message.answer(text = 'Салмагын жазыныз (см)',reply_markup=cancel_calc)
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
        if data.get('city') == 'KK':
            price_weight = PRICE_WEIGHT_KK
            price_volume = PRICE_VOLUME_KK
        elif data.get('city') == 'BISH':
            price_weight = PRICE_WEIGHT_BISH
            price_volume = PRICE_VOLUME_BISH
        volume_price = (data['width'] * data['height'] * data ['length'])/1000000 * price_volume
        weigth_price = data['weight'] * price_weight
        max_price = round(max(volume_price,weigth_price),1)
        data = await state.get_data()
        if data['language'] == 'RU':
            default_kb = default_kb_ru
            await message.answer(text = f'Ваша цена: {max_price} $',reply_markup=default_kb)
        else:
            default_kb = default_kb_kg
            await message.answer(text = f'Сиздин бааңыз: {max_price} $',reply_markup=default_kb)
        await state.set_state()
    elif message.text == 'Отмена':
        await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
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
    if callback.data == 'set_marketplace':
        await callback.message.answer(text = 'Выберите у какого маркетплейса хотите поменять ссылку/текст',reply_markup=set_marketplace.as_markup())
    if callback.data == 'set_prices':
        await callback.message.answer(text = 'Выберите у какой переменной хотите поменять значение',reply_markup=set_price.as_markup())


@dp.callback_query(lambda query: query.data.startswith('r_'))
async def set_market(callback:CallbackQuery,state:FSMContext):
    await state.update_data(data = {'data':callback.data[2:]})
    await callback.message.answer(text = f'Введите новую цену для маркетплейса {callback.data[2:]}')
    await state.set_state(Admin.set_price)


@dp.callback_query(lambda query: query.data == 'reset_password')
async def reset_password(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(text = 'Введите новый пароль')
    await state.update_data(data = {'data':'resetpassword'})
    await state.set_state(Admin.set_price)



@dp.callback_query(lambda query: query.data == 're_whatsapp')
async def re_whatsapp(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(text = 'Введите новую ссылку для Whatsapp')
    await state.update_data(data = {'data':'whatsapp'})
    await state.set_state(Admin.set_price)


@dp.callback_query(lambda query: query.data.startswith('p_'))
async def set_price_v(callback:CallbackQuery,state:FSMContext):
    await state.update_data(data = {'data':callback.data[8:]})
    await callback.message.answer(text = 'Введите новое значение')
    await state.set_state(Admin.set_price)


@dp.callback_query(lambda query: query.data == 'send_broadcast')
async def send_b(callback:CallbackQuery,state:FSMContext):
    await callback.message.answer(text = 'Введите новость')
    await state.set_state(Admin.news)


@dp.message(Admin.news)
async def send_new(message:Message,state:FSMContext):
    text = message.text
    await send_news(text)
    await message.answer(text = 'Новость успешно разослана')
    await state.set_state()


@dp.message(Admin.set_price)
async def set_price_v2(message:Message,state:FSMContext):
    data = await state.get_data()
    new_value = message.text
    global PRICE_VOLUME_BISH
    global PRICE_VOLUME_KK
    global PRICE_WEIGHT_BISH
    global PRICE_WEIGHT_KK
    global TAOBAO
    global ONE_AND_SIX
    global PINDUODUO
    global POIZON
    global LINK_WHATSAPP
    global ADMIN_PASSWORD
    if '_' in data['data']:
        if data['data'] == 'volume_bish':
            PRICE_VOLUME_BISH = float(new_value)
        elif data['data'] == 'volume_kk':
            PRICE_VOLUME_KK = float(new_value)
        elif data['data'] == 'weight_bish':
            PRICE_WEIGHT_BISH = float(new_value)
        elif data['data'] == 'weight_kk':
            PRICE_WEIGHT_KK == float(new_value)
        await message.answer(text = 'Вы успешно сменили цену')
    elif data['data'] == 'whatsapp':
        LINK_WHATSAPP = new_value
        await message.answer(text = 'Вы успешно сменили ссылку на whatsapp')
    elif data['data'] == 'resetpassword':
        ADMIN_PASSWORD = new_value
        await message.answer(text = 'Вы сменили пароль')
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



@dp.message(F.document)
async def handle_admin_documents(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.get("is_admin") == True:
        file_info = await bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        file = await bot.download_file(file_path)
        df = pd.read_excel(file,header = None)
        track_codes = df.iloc[:,0].to_list()
        data = df.iloc[:, :2]
        new_status = message.caption
        if new_status == 'На Складе':
            append_products(data)
            await message.answer('Все готово,проверьте')
        else:
            update_google_sheet(track_codes,new_status)
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
        await message.answer(text = 'Базар тандаңыз',reply_markup=instruction_kb.as_markup())


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




async def main():
    await dp.start_polling(bot)



asyncio.run(main())