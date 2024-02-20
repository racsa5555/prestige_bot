import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file('./credentials.json', scopes=scopes)
client = gspread.authorize(credentials)

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
    return orders_info

def find_order_by_track_code(track_code):
    spreadsheet = client.open(title='Users')
    sheets = spreadsheet.worksheets()
    sheet = sheets[0]
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0]) 
    item = df[df['Трек Код'] == track_code]
    status = item.iloc[0]['Статус']
    info = f'Трек-код: {track_code}, Статус: {status}'
    return info


def register_client(data):
    spreadsheet = client.open(title='Users')
    sheets = spreadsheet.worksheets()
    sheet = sheets[1]
    sheet.append_row([data['city'],data['full_name'] + ' ' + data['name'],data['phone_number'],data['id']])
    return True


# print(find_order_by_id('2000'))
# sheets = spreadsheet.worksheets()
# sheet = sheets[0]
# data = sheet.get_all_records()
# print(data)
