PRICE_WEIGHT_KK = 3.6  # для цены по весу в Караколе
PRICE_VOLUME_KK = 370 # для цены по обьему в Караколе

ADMIN_PASSWORD = '1'

LINK_WHATSAPP = ''


# ADRESS_KK = '👤 蓝天LT01-{}\n📞  15547009391\n{}: \n广东省广州市白云区江高镇南岗三元南路广新元素54号云创港1119-蓝天LT01库房-{} ({})'
ADRESS_KK = '刚子(6556)G-{}\n13089886002\n{}: \n广东省佛山市南海区里水镇海南洲工业区53号进门左手边第一家（6556) G-{} ({})'
PINDUODUO = 'link1'
TAOBAO = 'link2'
ONE_AND_SIX = 'link3' #1688
POIZON = 'link4'

def send_adress(id,phone_number,lang,city,ADRESS_KK):
    if lang == 'RU':
        if city == 'KK':
            return ADRESS_KK.format(id,'Полный адрес',id,phone_number)
    else:
        if city == 'KK':
            return ADRESS_KK.format(id,'Толук адрес',id,phone_number)
    

def send_profile(kwargs):
    if kwargs['language'] == 'RU':
        text = '📃Ваш профиль📃\n🪪 Персональный id: {}\n👤 Имя: {}\n👤 Фамилия: {}\n📞 Номер: {}\n🌍 Геопозиция: {}'
    if kwargs['language'] == 'KG':
        text = '📃Сиздин профилиниз📃\n🪪 Жеке id: {}\n👤 Аты: {}\n👤 Фамилия: {}\n📞 Номер: {}\n🌍 Турган жери: {}'
    if kwargs["city"] == 'KK':
        city = 'Каракуль'

    if kwargs['language'] == 'RU':
        return text.format(kwargs['id'], kwargs['name'], kwargs['full_name'], kwargs['phone_number'], city)
    elif kwargs['language'] == 'KG':
        return text.format(kwargs['id'], kwargs['name'], kwargs['full_name'], kwargs['phone_number'], city)

def cancel_sender(lang):
    if lang == 'RU':
        return f'Вы отменили последнее действие'
    else:
        return f'Акыркы аракетиңизди артка кайтардыңыз'
    