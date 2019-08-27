import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)

sheet = client.open("IGPost").sheet1


def append(username,service_type,quantity,last_post):
    sheet.append_row([username, service_type, quantity, last_post])


def add_address(address):
    email = 'esocialpanel@gmail.com'
    for num, email in enumerate(sheet.cell(num, 3)):
        print('{}:{}'.format(num+1, email))
        sheet.update_cell(num+1, 3, f'address for {email}')
    #return num, email


def get_all_sheets():
    useremail = sheet.col_values(1)
    userid = sheet.col_values(2)
    temp_list = dict(zip(useremail, userid))
    return temp_list


def get_sheets():
    emails = []
    ids = []
    addresses = []
    list_of_lists = sheet.get_all_values()
    for user in list_of_lists:
        email = user[0]
        id = user[1]
        address = user[2]
        emails.append(email)
        ids.append(id)
        addresses.append(address)
    return emails, ids, addresses


def get_sh():
    username = []  
    service_type = []
    quantity = []
    last_post = []
    list_of_lists = sheet.get_all_values()
    for user in list_of_lists:
        username = user[0]
        service_type = user[1]
        quantity = user[2]
        last_post = user[3]
        username.append(username)
        service_type.append(service_type)
        quantity.append(quantity)
        last_post.append(last_post)
    return username, service_type, quantity, last_post
