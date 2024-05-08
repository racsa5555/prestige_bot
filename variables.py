PRICE_WEIGHT_BISH = 4.4  # для цены по весу в Караколе
PRICE_VOLUME_BISH = 370 # для цены по обьему в Караколе
PRICE_WEIGHT_TOKMOK = 4.4  # для цены по весу в Караколе
PRICE_VOLUME_TOKMOK = 370 # для цены по обьему в Караколе
PRICE_WEIGHT_OSH = 4.4  # для цены по весу в Караколе
PRICE_VOLUME_OSH = 370 # для цены по обьему в Караколе
PRICE_WEIGHT_GULCHO = 4.4  # для цены по весу в Караколе
PRICE_VOLUME_GULCHO = 370 # для цены по обьему в Караколе
PRICE_WEIGHT_SOKULUK = 4.4  # для цены по весу в Караколе
PRICE_VOLUME_SOKULUK = 370 # для цены по обьему в Караколе
# для цены по обьему в Бишкеке

ADMIN_PASSWORD = '1'

LINK_WHATSAPP = 'https://wa.me/+996708999963'


ADRESS_OSH = '👤怡宝YBS-{}\n☎️ 15147091118\n{}: \n广东省广州市白云区江高镇南岗三元南路62号安托仓储1119怡宝YBS库房-{} ({})\nПочтовый индекс: 510440'
ADRESS_BISH = '👤怡宝YBS-{}\n☎️ 15147091118\n{}: \n广东省广州市白云区江高镇南岗三元南路62号安托仓储1119怡宝YBS库房-{} ({})\nПочтовый индекс: 510440'
ADRESS_TOKMOK = '👤怡宝YBS-{}\n☎️ 15147091118\n{}: \n广东省广州市白云区江高镇南岗三元南路62号安托仓储1119怡宝YBS库房-{} ({})\nПочтовый индекс: 510440'
ADRESS_SOKULUK = '👤怡宝YBS-{}\n☎️ 15147091118\n{}: \n广东省广州市白云区江高镇南岗三元南路62号安托仓储1119怡宝YBS库房-{} ({})\nПочтовый индекс: 510440'
ADRESS_GULCHO = '👤怡宝YBS-{}\n☎️ 15147091118\n{}: \n广东省广州市白云区江高镇南岗三元南路62号安托仓储1119怡宝YBS库房-{} ({})\nПочтовый индекс: 510440'


PINDUODUO = 'link1'
TAOBAO = 'link2'
ONE_AND_SIX = 'link3' #1688
POIZON = 'link4'

def send_adress(id,phone_number,lang,city,ADRESS_BISH,ADRESS_OSH,ADRESS_TOKMOK,ADRESS_SOKULUK,ADRESS_GULCHO):
    if lang == 'RU':
        if city == 'BISH':
            return ADRESS_BISH.format(id,'Полный адрес',id,phone_number)
        elif city == 'SOKULUK':
            return ADRESS_SOKULUK.format(id,'Полный адрес',id,phone_number)
        elif city == 'OSH':
            return ADRESS_OSH.format(id,'Полный адрес',id,phone_number)
        elif city == 'TOKMOK':
            return ADRESS_TOKMOK.format(id,'Полный адрес',id,phone_number)
        elif city == 'GULCHO':
            return ADRESS_GULCHO.format(id,'Полный адрес',id,phone_number)
    else:
        if city == 'BISH':
            return ADRESS_BISH.format(id,'Толук адрес',id,phone_number)
        elif city == 'SOKULUK':
            return ADRESS_SOKULUK.format(id,'Толук адрес',id,phone_number)
        elif city == 'OSH':
            return ADRESS_OSH.format(id,'Толук адрес',id,phone_number)
        elif city == 'TOKMOK':
            return ADRESS_TOKMOK.format(id,'Толук адрес',id,phone_number)
        elif city == 'GULCHO':
            return ADRESS_GULCHO.format(id,'Толук адрес',id,phone_number)
    

def send_profile(kwargs):
    if kwargs['language'] == 'RU':
        text = '📃Ваш профиль📃\n🪪 Персональный id: {}\n👤 Имя: {}\n👤 Фамилия: {}\n📞 Номер: {}\n🌍 Геопозиция: {}'
    if kwargs['language'] == 'KG':
        text = '📃Сиздин профилиниз📃\n🪪 Жеке id: {}\n👤 Аты: {}\n👤 Фамилия: {}\n📞 Номер: {}\n🌍 Турган жери: {}'
    if kwargs["city"] == 'BISH':
        city = 'Бишкек'
    elif kwargs["city"] == 'OSH':
        city = 'Ош'
    elif kwargs["city"] == 'SOKULUK':
        city = 'Сокулук'
    elif kwargs["city"] == 'TOKMOK':
        city = 'Токмок'
    elif kwargs["city"] == 'GULCHO':
        city = 'Гулчо'

    if kwargs['language'] == 'RU':
        return text.format(kwargs['id'], kwargs['name'], kwargs['full_name'], kwargs['phone_number'], city)
    elif kwargs['language'] == 'KG':
        return text.format(kwargs['id'], kwargs['name'], kwargs['full_name'], kwargs['phone_number'], city)

def cancel_sender(lang):
    if lang == 'RU':
        return f'Вы отменили последнее действие'
    else:
        return f'Акыркы аракетиңизди артка кайтардыңыз'
    