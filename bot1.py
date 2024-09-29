import telebot
from telebot import types
import psycopg2
import os

# متغيرات لتخزين تفاصيل قاعدة البيانات
DB_HOST = os.getenv('STACKHERO_POSTGRESQL_HOST')
DB_NAME = os.getenv('STACKHERO_POSTGRESQL_DB')
DB_USER = os.getenv('STACKHERO_POSTGRESQL_USER')
DB_PASSWORD = os.getenv('STACKHERO_POSTGRESQL_PASSWORD')

# الاتصال بقاعدة البيانات
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode='require'
    )

# أدخل مفتاح API الخاص بالبوت هنا
bot = telebot.TeleBot("8090786845:AAFwLA0VEVphRorM31fyY44iMyXXK1EO9c0")

# تابع لتنفيذ الأمر /start عند الضغط عليه
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    
    # جلب الرصيد من قاعدة البيانات
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT balance FROM user_balances WHERE user_id = %s", (message.from_user.id,))
            result = cursor.fetchone()
            account_balance = result[0] if result else 0

    # إنشاء زر شفاف لعرض الرصيد
    button = types.InlineKeyboardButton(f"رصيد: {account_balance}", callback_data='balance')
    markup.add(button)

    bot.send_message(message.chat.id,
                     'مرحبا بك في متجر الخدمات الإلكترونية!\n',
                     reply_markup=markup)

# تابع لمعالجة الضغط على الزر
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'balance':
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT balance FROM user_balances WHERE user_id = %s", (call.from_user.id,))
                result = cursor.fetchone()
                account_balance = result[0] if result else 0

        bot.answer_callback_query(call.id, text=f"رصيدك الحالي هو: {account_balance}")

# بدء البوت
bot.polling(non_stop=True)
