import datetime
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from gspread_formatting import Color, CellFormat,format_cell_range

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file('./credentials.json', scopes=scopes)
client = gspread.authorize(credentials)

def append_products(df):
    sheet = client.open(title = 'Amanat').sheet1
    date = datetime.datetime.now()
    current_date = date.strftime("%m-%d")
    values = df.values.tolist()
    for row in values:
        row.append('На Складе')
        row.append(current_date)
        row = [str(value) for value in row]
    sheet.append_rows(values)
    return True

def update_google_sheet(track_codes, new_status):
    sheet = client.open(title = 'Amanat').sheet1 
    data = sheet.get_all_records()
    date = datetime.datetime.now()
    current_date = date.strftime("%m-%d")
    for row in data:
        if row['Трек Код'] in track_codes:
            row['Статус'] = new_status
            row['Дата'] = current_date
    add_track_codes = {code for code in track_codes if code not in {row['Трек Код'] for row in data}}
    current_row = len(sheet.get_all_records())+2
    last_row = current_row-1
    if add_track_codes:
        for code in add_track_codes:
            sheet.append_row([code])
            last_row += 1
    if add_track_codes:
        diapazon = f'A{current_row}:A{last_row}'
        sheet.format(diapazon,{"backgroundColor": {"red": 1.0}})
    sheet.update([list(data[0].keys())] + [list(row.values()) for row in data])
    return True


def find_order_by_id(item_id,lang):
    spreadsheet = client.open(title='Amanat')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0]) 
    items = df[df['Код клиента'] == item_id]  
    orders_info = ""
    k = 0
    for index, row in items.iterrows():
        if row['Статус'] == 'В Пути':
            status = '🚛 В Пути'
        if row['Статус'] == 'На Складе':
            status = '🏬 На Складе'
        if row['Статус'] == 'В КР':
            status = '🇰🇬 в КР'
        orders_info += f"Код: {row['Трек Код']}, {status}\nДата: {row['Дата']}\n———————————————-\n"
    if orders_info:
        return orders_info
    if lang == 'RU':
        return f"У вас пока-что нет товаров"
    else:
        return f"Сизде товар жок"

def find_order_by_track_code(track_code,lang):
    track_code = str(track_code)  
    spreadsheet = client.open(title='Amanat')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0]) 
    item = df[df['Трек Код'] == track_code]
    if not item.empty:
        status = item.iloc[0]['Статус']
        time = item.iloc[0]['Дата']
        if status == 'В Пути':
            status = '🚛 В Пути'
        if status == 'На Складе':
            status = '🏬 На Складе'
        if status == 'В КР':
            status = '🇰🇬 в КР'
        info = f'Код: {track_code}, {status}\nДата: {time}\n'
        return info
    if lang == 'RU':
        return 'Товар с таким трек-кодом не найден в базе'
    else:
        return 'Бул товар табылганжок'

def register_client(data):
    spreadsheet = client.open(title='Amanat')
    sheets = spreadsheet.worksheets()
    sheet = sheets[1]
    sheet.append_row([data['city'],data['full_name'] + ' ' + data['name'],data['phone_number'],data['id']])
    return True

def update_client_by_id(client_id, new_data):
    spreadsheet = client.open('Amanat')
    sheets = spreadsheet.worksheets()
    sheet = sheets[1]
    data = sheet.get_all_records()
    for i, row in enumerate(data, start=2):
        if row['id'] == client_id:
            for key, value in new_data.items():
                sheet.update_cell(i, sheet.find(key).col, value)
            return True
    return False

def find_user_by_data(phone_number,client_id,lang):
    spreadsheet = client.open('Amanat')
    sheets = spreadsheet.worksheets()
    sheet = sheets[1]
    data = sheet.get_all_records()
    for i, row in enumerate(data, start=2):
        if row['id'] == int(client_id) and row['Номер'] == int(phone_number):
            data = {'id':client_id,
                    'name':row['ФИО'].split()[0],
                    'full_name':row['ФИО'].split()[1],
                    'phone_number':row['Город'],
                    'city':row['Город'],
                    'language':lang
                    }
            return data
    if lang == 'RU':
        return 'Извините, неверный номер или код'
    else:
        return 'Кечиресиз, номер же жеке код туура эмес'

    


