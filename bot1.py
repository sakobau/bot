import os
import telebot
from google.oauth2 import service_account
from googleapiclient.discovery import build

# توكن البوت
TOKEN = '7918486703:AAFlQxZtkKxENYRZ8T96ZZ1BW7Jo2ez88Yw'
bot = telebot.TeleBot(TOKEN)

# إعداد بيانات الاعتماد من ملف JSON
SERVICE_ACCOUNT_FILE = 'path_to_your_json_file.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# إعداد الاتصال بـ Google Sheets
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# ID الجدول الخاص بك من Google Sheets
SPREADSHEET_ID = 'Google Sheet ID الخاص بك'

service = build('sheets', 'v4', credentials=credentials)

# الدالة التي تضيف بيانات إلى Google Sheet
def add_data_to_sheet(data):
    sheet = service.spreadsheets()
    body = {
        'values': [data]
    }
    result = sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A1",  # تعديل النطاق حسب احتياجاتك
        valueInputOption="RAW",
        body=body
    ).execute()
    return result

# الدالة التي تتعامل مع رسائل المستخدمين
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "أهلاً! أرسل لي البيانات التي تريد إضافتها إلى Google Forms.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_data = [message.chat.username, message.text]
    add_data_to_sheet(user_data)
    bot.send_message(message.chat.id, "تم حفظ البيانات بنجاح!")

# تشغيل البوت
bot.polling()
