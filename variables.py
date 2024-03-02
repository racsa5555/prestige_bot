PRICE_WEIGHT_KK = 4.4  # для цены по весу в Караколе
PRICE_WEIGHT_BISH = 3.8 # для цены по весу в Бишкеке
PRICE_VOLUME_KK = 370 # для цены по обьему в Караколе
PRICE_VOLUME_BISH = 330 # для цены по обьему в Бишкеке

ADMIN_PASSWORD = '1'

LINK_WHATSAPP = 'https://wa.me/+996507851004'


ADRESS_KK = '👤 蓝天LT01-{}\n📞  15547009391\n{}: \n广东省广州市白云区江高镇南岗三元南路广新元素54号云创港1119-蓝天LT01库房-{} ({})'
ADRESS_BISH = '👤 蓝天LT01-{}\n📞  15547009391\n{}: \n广东省广州市白云区江高镇南岗三元南路广新元素54号云创港1119-蓝天LT01库房-{} ({})'


PINDUODUO = 'link1'
TAOBAO = 'link2'
ONE_AND_SIX = 'link3' #1688
POIZON = 'link4'

def send_adress(id,phone_number,lang,city,ADRESS_KK,ADRESS_BISH):
    if lang == 'RU':
        if city == 'KK':
            return ADRESS_KK.format(id,'Полный адрес',id,phone_number)
        elif city == 'BISH':
            return ADRESS_BISH.format(id,'Полный адрес',id,phone_number)
    else:
        if city == 'KK':
            return ADRESS_KK.format(id,'Толук адрес',id,phone_number)
        elif city == 'BISH':
            return ADRESS_BISH.format(id,'Толук адрес',id,phone_number)
    

def send_profile(kwargs):
    if kwargs['language'] == 'RU':
        if kwargs["city"] == 'KK':
            city = 'Каракол'
        else:
            city = 'Бишкек'
        return f'📃Ваш профиль📃\n🪪 Персональный id: {kwargs["id"]}\n👤 Имя: {kwargs["name"]}\n👤 Фамилия: {kwargs["full_name"]}\n📞 Номер: {kwargs["phone_number"]}\n🌍 Геопозиция: {city}'
    else:
        if kwargs["city"] == 'KK':
            city = 'Каракол'
        else:
            city = 'Бишкек'
        return f'📃Сиздин профилиниз📃\n🪪 Жеке id: {kwargs["id"]}\n👤 Аты: {kwargs["name"]}\n👤 Фамилия: {kwargs["full_name"]}\n📞 Номер: {kwargs["phone_number"]}\n🌍 Турган жери: {city}'

def cancel_sender(lang):
    if lang == 'RU':
        return f'Вы отменили последнее действие'
    else:
        return f'Акыркы аракетиңизди артка кайтардыңыз'