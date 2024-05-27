PRICE_WEIGHT_BISH = 4.4  # для цены по весу в Караколе
PRICE_VOLUME_BISH = 370 # для цены по обьему в Караколе
PRICE_WEIGHT_TALAS = 4.4  # для цены по весу в ТОКМОК
PRICE_VOLUME_TALAS = 370 # для цены по обьему в ТОКМОК
PRICE_WEIGHT_OSH = 4.4  # для цены по весу в Караколе
PRICE_VOLUME_OSH = 370 # для цены по обьему в Караколе
PRICE_WEIGHT_JL = 4.4  # для цены по весу в ГУЛЧО
PRICE_VOLUME_JL = 370 # для цены по обьему в ГУЛЧО
PRICE_WEIGHT_UZ = 4.4  # для цены по весу в СОКУЛУК
PRICE_VOLUME_UZ = 370 # для цены по обьему в СОКУЛУК
PRICE_WEIGHT_TASH = 4.4  # для цены по весу в СОКУЛУК
PRICE_VOLUME_TASH = 370 # для цены по обьему в СОКУЛУК
PRICE_WEIGHT_NOOKAT = 4.4  # для цены по весу в СОКУЛУК
PRICE_VOLUME_NOOKAT = 370 # для цены по обьему в СОКУЛУК
PRICE_WEIGHT_BATKEN = 4.4  # для цены по весу в СОКУЛУК
PRICE_VOLUME_BATKEN = 370 # для цены по обьему в СОКУЛУК
PRICE_WEIGHT_EKA = 4.4  # для цены по весу в СОКУЛУК
PRICE_VOLUME_EKA = 370 # для цены по обьему в СОКУЛУК
PRICE_WEIGHT_MSK = 4.4  # для цены по весу в СОКУЛУК
PRICE_VOLUME_MSK = 370 # для цены по обьему в СОКУЛУК

ADMIN_PASSWORD = '1'

LINK_WHATSAPP = 'https://wa.me/+996708999963'


ADRESS_OSH = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000'
ADRESS_BISH = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000'
ADRESS_TALAS = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000'
ADRESS_UZ = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000'
ADRESS_JL = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000'
ADRESS_MSK = '阿辉A578-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-A578-{} ({})\nПочтовый индекс: 3220000'
ADRESS_EKA = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000'
ADRESS_BATKEN = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000'
ADRESS_NOOKAT = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000'
ADRESS_TASH = '阿辉M115-{}\n18727306620\n{}: \n浙江省金华市义乌市北苑街道凌云八区59栋3单元-M115-{}({})\nПочтовый индекс: 3220000'

PINDUODUO = 'link1'
TAOBAO = 'link2'
ONE_AND_SIX = 'link3' #1688
POIZON = 'link4'

def send_adress(id,phone_number,lang,city,ADRESS_BISH,ADRESS_OSH,ADRESS_TALAS,ADRESS_UZ,ADRESS_JL,ADRESS_MSK,ADRESS_EKA,ADRESS_BATKEN,ADRESS_NOOKAT,ADRESS_TASH):
    if lang == 'RU':
        if city == 'BISH':
            return ADRESS_BISH.format(id,'Полный адрес',id,phone_number)
        elif city == 'UZ':
            return ADRESS_UZ.format(id,'Полный адрес',id,phone_number)
        elif city == 'OSH':
            return ADRESS_OSH.format(id,'Полный адрес',id,phone_number)
        elif city == 'TALAS':
            return ADRESS_TALAS.format(id,'Полный адрес',id,phone_number)
        elif city == 'JL':
            return ADRESS_JL.format(id,'Полный адрес',id,phone_number)
        elif city == 'MSK':
            return ADRESS_MSK.format(id,'Полный адрес',id,phone_number)
        elif city == 'EKA':
            return ADRESS_EKA.format(id,'Полный адрес',id,phone_number)
        elif city == 'BATKEN':
            return ADRESS_BATKEN.format(id,'Полный адрес',id,phone_number)
        elif city == 'NOOKAT':
            return ADRESS_NOOKAT.format(id,'Полный адрес',id,phone_number)
        elif city == 'TASH':
            return ADRESS_TASH.format(id,'Полный адрес',id,phone_number)
    else:
        if city == 'BISH':
            return ADRESS_BISH.format(id,'Толук адрес',id,phone_number)
        elif city == 'UZ':
            return ADRESS_UZ.format(id,'Толук адрес',id,phone_number)
        elif city == 'OSH':
            return ADRESS_OSH.format(id,'Толук адрес',id,phone_number)
        elif city == 'TALAS':
            return ADRESS_TALAS.format(id,'Толук адрес',id,phone_number)
        elif city == 'JL':
            return ADRESS_JL.format(id,'Толук адрес',id,phone_number)
        elif city == 'MSK':
            return ADRESS_MSK.format(id,'Толук адрес',id,phone_number)
        elif city == 'EKA':
            return ADRESS_EKA.format(id,'Толук адрес',id,phone_number)
        elif city == 'BATKEN':
            return ADRESS_BATKEN.format(id,'Толук адрес',id,phone_number)
        elif city == 'NOOKAT':
            return ADRESS_NOOKAT.format(id,'Толук адрес',id,phone_number)
        elif city == 'TASH':
            return ADRESS_TASH.format(id,'Толук адрес',id,phone_number)
    

def send_profile(kwargs):
    if kwargs['language'] == 'RU':
        text = '📃Ваш профиль📃\n🪪 Персональный id: {}\n👤 Имя: {}\n👤 Фамилия: {}\n📞 Номер: {}\n🌍 Геопозиция: {}'
    if kwargs['language'] == 'KG':
        text = '📃Сиздин профилиниз📃\n🪪 Жеке id: {}\n👤 Аты: {}\n👤 Фамилия: {}\n📞 Номер: {}\n🌍 Турган жери: {}'
    if kwargs["city"] == 'BISH':
        city = 'Бишкек'
    elif kwargs["city"] == 'OSH':
        city = 'Ош'
    elif kwargs["city"] == 'UZ':
        city = 'Узген'
    elif kwargs["city"] == 'TA':
        city = 'Талас'
    elif kwargs["city"] == 'JL':
        city = 'Жалал-Абад'
    elif kwargs["city"] == 'TASH':
        city = 'Таш-Комур'
    elif kwargs["city"] == 'N':
        city = 'Ноокат'
    elif kwargs["city"] == 'BAT':
        city = 'Баткен'
    elif kwargs["city"] == 'MOS':
        city = 'Москва'
    elif kwargs["city"] == 'EKA':
        city = 'Екатеринбург'

    if kwargs['language'] == 'RU':
        return text.format(kwargs['id'], kwargs['name'], kwargs['full_name'], kwargs['phone_number'], city)
    elif kwargs['language'] == 'KG':
        return text.format(kwargs['id'], kwargs['name'], kwargs['full_name'], kwargs['phone_number'], city)

def cancel_sender(lang):
    if lang == 'RU':
        return f'Вы отменили последнее действие'
    else:
        return f'Акыркы аракетиңизди артка кайтардыңыз'
    