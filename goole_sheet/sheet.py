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


def update_google_sheet(track_codes, new_status):
    sheet = client.open(title = 'Users').sheet1 
    data = sheet.get_all_records()
    for row in data:
        if row['Трек Код'] in track_codes:
            track_code = row['Трек Код']
            track_codes.remove(track_code)
            row['Статус'] = new_status

    current_row = len(sheet.get_all_records())+2
    last_row = current_row
    print(track_codes)
    for code in track_codes:
        sheet.append_row([code])
        last_row += 1
    
    last_row-=1
    print(current_row,last_row)
    diapazon = f'A{current_row}:A{last_row}'
    sheet.format(diapazon,{"backgroundColor": {"red": 1.0}})
    sheet.update([list(data[0].keys())] + [list(row.values()) for row in data])
    return True


def find_order_by_id(item_id):
    spreadsheet = client.open(title='Users')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0]) 
    items = df[df['Код клиента'] == item_id]  
    orders_info = ""
    for index, row in items.iterrows():
        orders_info += f"Трек-код: {row['Трек Код']}, Статус: {row['Статус']}\n"
    if orders_info:
        return orders_info
    return f"У вас пока что нет товаров"

def find_order_by_track_code(track_code):
    track_code = str(track_code)  
    spreadsheet = client.open(title='Users')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0]) 
    item = df[df['Трек Код'] == track_code]
    if not item.empty:
        status = item.iloc[0]['Статус']
        info = f'Трек-код: {track_code}, Статус: {status}'
        return info
    return 'Товар с таким трек-кодом не найден в базе'

def register_client(data):
    spreadsheet = client.open(title='Users')
    sheets = spreadsheet.worksheets()
    sheet = sheets[1]
    sheet.append_row([data['city'],data['full_name'] + ' ' + data['name'],data['phone_number'],data['id']])
    return True

def update_client_by_id(client_id, new_data):
    spreadsheet = client.open('Users')
    sheets = spreadsheet.worksheets()
    sheet = sheets[1]
    data = sheet.get_all_records()
    for i, row in enumerate(data, start=2):
        if row['id'] == client_id:
            for key, value in new_data.items():
                sheet.update_cell(i, sheet.find(key).col, value)
            return True
    return False 

