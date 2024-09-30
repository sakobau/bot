import telebot
from telebot import types
import psycopg2
import os

# متغير لتخزين الرابط الكامل لقاعدة البيانات (Heroku)
DATABASE_URL = os.getenv('DATABASE_URL')  # متغير البيئة الخاص بقاعدة بيانات Heroku

# الاتصال بقاعدة البيانات باستخدام الرابط الكامل
def connect_db():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# أدخل مفتاح API الخاص بالبوت هنا
API_TOKEN = "8090786845:AAFwLA0VEVphRorM31fyY44iMyXXK1EO9c0"
bot = telebot.TeleBot(API_TOKEN)

# إنشاء الجدول إذا لم يكن موجودًا
def create_table():
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''CREATE TABLE IF NOT EXISTS user_balances (
                user_id BIGINT PRIMARY KEY,
                balance INT DEFAULT 0
            );''')
            conn.commit()

# تابع لتنفيذ الأمر /start عند الضغط عليه
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    
    # جلب الرصيد من قاعدة البيانات
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT balance FROM user_balances WHERE user_id = %s", (message.from_user.id,))
            result = cursor.fetchone()
            if result:
                account_balance = result[0]
            else:
                # إضافة مستخدم جديد إذا لم يكن موجودًا في قاعدة البيانات
                cursor.execute("INSERT INTO user_balances (user_id) VALUES (%s)", (message.from_user.id,))
                conn.commit()
                account_balance = 0

    # إنشاء زر شفاف لعرض الرصيد
    button = types.InlineKeyboardButton(f"رصيد: {account_balance}", callback_data='balance')
    markup.add(button)

    bot.send_message(message.chat.id,
                     'مرحبا بك في بوت الخدمة!\n',
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

# تابع لشحن الرصيد (يمكنك تخصيصه بناءً على متطلباتك)
@bot.message_handler(commands=['topup'])
def top_up(message):
    if message.text.startswith('/topup'):
        try:
            amount = int(message.text.split()[1])
            with connect_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("UPDATE user_balances SET balance = balance + %s WHERE user_id = %s", (amount, message.from_user.id))
                    conn.commit()
            
            bot.reply_to(message, f"تم شحن رصيدك بمقدار {amount}.")
        except (IndexError, ValueError):
            bot.reply_to(message, "يرجى إدخال المبلغ بشكل صحيح بعد الأمر.")

# بدء البوت
create_table()  # إنشاء الجدول إذا لم يكن موجودًا
bot.polling(non_stop=True)
