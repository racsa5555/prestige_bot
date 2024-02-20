import asyncio 
from typing import Any, Dict

from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.types import Message,CallbackQuery
from aiogram.filters import CommandStart
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.enums import MessageEntityType

from decouple import config

from goole_sheet import register_client,find_order_by_id
from states import UserState,Calculator
from kbds import set_city_kb,profile_kb,default_kb,cancel_calc,tracking_kb,admin_kb

TOKEN = config('TOKEN')

bot = Bot(TOKEN)

dp = Dispatcher()

id = 2000


@dp.callback_query(lambda query: query.data == 'update_profile')
async def set_bish(callback:CallbackQuery,state:FSMContext):
    await state.update_data(update = True)
    await callback.message.answer(text = 'Вы с города или региона',reply_markup=set_city_kb.as_markup())

@dp.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    await message.answer(text = 'Здравствуйте 👋\nПеред использованием бота нужно пройти регистрацию 😎')
    await message.answer(text = 'С какого Вы города',reply_markup=set_city_kb.as_markup())

@dp.callback_query(lambda query: query.data.startswith('city_set'))
async def set_bish(callback:CallbackQuery,state:FSMContext):
    if callback.data == 'city_set_ik':
        await state.update_data(city = 'IK')
    else:
        await state.update_data(city = 'BISH')
    await callback.message.answer(text = 'Как вас зовут')
    await state.set_state(UserState.name)

@dp.message(UserState.name)
async def set_name(message:Message,state:FSMContext):
    await state.update_data(name = message.text)
    await state.set_state(UserState.full_name)
    await message.answer(text = 'Как ваша фамилия')


@dp.message(UserState.full_name)
async def set_full_name(message:Message,state:FSMContext):
    await state.update_data(full_name = message.text)
    await state.set_state(UserState.phone_number)
    await message.answer(text = 'Пожалуйста, напишите номер телефона,\nпример: без плюса 996XXXXXXXXX')


@dp.message(UserState.phone_number)
async def set_full_name(message:Message,state:FSMContext):
    if message.text.isdigit() and len(message.text) == 9:
        await state.update_data(phone_number = message.text)
        data = await state.get_data()
        update =  data.get('update')
        if update == True:
            await message.answer(text = '✅ Успешное обновление профиля !',reply_markup=default_kb)
            await message.answer(text = f'📃Ваш профиль📃\n🪪 Персональный id: {data["id"]}\n👤 Имя: {data["name"]}\n👤 Фамилия: {data["full_name"]}\n📞 Номер: {data["phone_number"]}\n🌍 Геопозиция: {data["city"]}',reply_markup=profile_kb.as_markup())
            await state.set_state()
        else:
            global id
            await state.update_data(id = id)
            id+=1
            data = await state.get_data()
            await message.answer(text = '✅ Успешная регистрация !',reply_markup=default_kb)
            await message.answer(text = f'📃Ваш профиль📃\n🪪 Персональный id: {data["id"]}\n👤 Имя: {data["name"]}\n👤 Фамилия: {data["full_name"]}\n📞 Номер: {data["phone_number"]}\n🌍 Геопозиция: {data["city"]}',reply_markup=profile_kb.as_markup())
            register_client(data)
            await state.set_state()
            
    else:
        await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')

@dp.message(F.text == 'Профиль')
async def get_profile(message:Message,state:FSMContext):
    data = await state.get_data()
    await message.answer(text = f'📃Ваш профиль📃\n🪪 Персональный id: {data["id"]}\n👤 Имя: {data["name"]}\n👤 Фамилия: {data["full_name"]}\n📞 Номер: {data["phone_number"]}\n🌍 Геопозиция: {data["city"]}',reply_markup=profile_kb.as_markup())


@dp.message(F.text == 'Адреса')
async def get_profile(message:Message,state:FSMContext):
    data = await state.get_data()
    await message.answer(text = f'👤 蓝天{data["city"]}-{data["id"]}\n📞  15547009391\nПолный адрес: \n广东省广州市白云区江高镇南岗三元南路广新元素54号云创港1119-蓝天LT01库房-{data["id"]} {data["phone_number"]}',reply_markup=profile_kb.as_markup())

@dp.message(F.text == 'Калькулятор')
async def set_length(message:Message,state:FSMContext):
    await message.answer(text = 'Введите длину (см)',reply_markup=cancel_calc)
    await state.set_state(Calculator.length)

@dp.message(Calculator.length)
async def set_length(message:Message,state:FSMContext):
    if message.text.isdigit():
        await state.update_data(length = int(message.text))
        await message.answer(text = 'Введите ширину (см)',reply_markup=cancel_calc)
        await state.set_state(Calculator.width)
    elif message.text == 'Отмена':
        await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
        await state.set_state()
    else:
        await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')

@dp.message(Calculator.width)
async def set_width(message:Message,state:FSMContext):
    if message.text.isdigit():
        await state.update_data(width = int(message.text))
        await message.answer(text = 'Введите высоту (см)',reply_markup=cancel_calc)
        await state.set_state(Calculator.height)
    elif message.text == 'Отмена':
        await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
        await state.set_state()
    else:
        await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')

@dp.message(Calculator.height)
async def set_height(message:Message,state:FSMContext):
    if message.text.isdigit():
        await state.update_data(height = int(message.text))
        await message.answer(text = 'Введите вес (кг)',reply_markup=cancel_calc)
        await state.set_state(Calculator.weight)
    elif message.text == 'Отмена':
        await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
        await state.set_state()
    else:
        await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')

@dp.message(F.text == 'Отмена')
async def cancel(message:Message,state:FSMContext):
    await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
    await state.set_state()


@dp.message(Calculator.weight)
async def set_width(message:Message,state:FSMContext):
    if message.text.isdigit():
        await state.update_data(weight = int(message.text))
        data = await state.get_data()
        if data.get('city') == 'IK':
            price_weight = 4.4
            price_volume = 370
        elif data.get('city') == 'BISH':
            price_weight = 3.8
            price_volume = 330
        volume_price = (data['width'] * data['height'] * data ['length'])/1000000 * price_volume
        weigth_price = data['weight'] * price_weight
        max_price = max(volume_price,weigth_price)
        await message.answer(text = f'Ваша цена: {max_price}',reply_markup=default_kb)
        await state.set_state()
    elif message.text == 'Отмена':
        await message.answer(text = 'Вы отменили последнее действие',reply_markup=default_kb)
        await state.set_state()
    else:
        await message.answer('❗️ Неверный формат ввода ❗️\nПопробуйте снова')



@dp.message(F.text == 'Отслеживание')
async def tracking(message:Message,state:FSMContext):
    await message.answer(text = 'Выберите способ отслеживания',reply_markup=tracking_kb.as_markup())

@dp.callback_query(lambda query: query.data == 'client_id')
async def tracking_by_client_id(callback:CallbackQuery,state:FSMContext):
    data = await state.get_data()
    client_id = data.get('id')
    res = find_order_by_id(str(client_id))
    await callback.message.answer(text = res)


# @dp.callback_query(lambda query: query.data == 'track-code')
# async def tracking_by_client_id(callback:CallbackQuery,state:FSMContext):
#     callback.message.answer(text = 'Введите трек-код товара')
#     pass

@dp.message(F.text == '6474184256:AAFqSpjtg32avQ5wmV26QwdOWwaPpKMn_qo')
async def admin(message:Message):
    await message.answer(text = 'Вы вошли в режим администратора',reply_markup=admin_kb)


@dp.message(F.document)
async def doc(message:Message):
    await message.answer(text = 'Вы отправили документ')








    


async def main():
    await dp.start_polling(bot)



asyncio.run(main())