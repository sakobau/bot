import telebot
from telebot import types
import psycopg2
import os

# متغير لتخزين تفاصيل قاعدة البيانات (تأكد من إعداد المتغيرات البيئية على هيروكو)
DATABASE_URL = os.getenv('DATABASE_URL')

# الاتصال بقاعدة البيانات
def connect_db():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

# اسم المستخدم الخاص بالمطور الذي يمكنه تعبئة الرصيد
developer_username = "m_55mg"  # استبدل بـ اسم المستخدم الخاص بالمطور

# أدخل مفتاح API الخاص بالبوت هنا
bot = telebot.TeleBot("8131016207:AAHC6QQIHw48c-XHCRQAYMOKk5PUu3n3vws")

# تابع لتنفيذ الأمر /start عند الضغط عليه
@bot.message_handler(commands=['start'])
def start(message):
    # إنشاء الأزرار
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # جلب الرصيد من قاعدة البيانات
    with connect_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT balance FROM user_balances WHERE user_id = %s", (message.from_user.id,))
            result = cursor.fetchone()
            if result:
                account_balance = result[0]
            else:
                account_balance = 0

    # إنشاء الأزرار مع الرصيد
    button1 = types.InlineKeyboardButton(f"رصيد حسابي: {account_balance}", callback_data='balance')
    button2 = types.InlineKeyboardButton("تعبئة رصيد حسابي", callback_data='top_up')
    button3 = types.InlineKeyboardButton("كارت هاتف", callback_data='mobile_card')
    button4 = types.InlineKeyboardButton("كارت شحن العاب", callback_data='game_card')
    button5 = types.InlineKeyboardButton("كارت تطبيقات", callback_data='app_card')

    # إضافة الأزرار إلى اللوحة
    markup.add(button1, button2, button3, button4, button5)
    
    # إرسال رسالة مع الكليشة والأزرار
    bot.send_message(message.chat.id,
                     'مرحبا بك في متجر ســـــــــــوبر تــــــكنو للخدمات الالكترونية\n'
                     'للاستفسار مراسلة المطور @m_55mg',
                     reply_markup=markup)

# تابع لتحديث رصيد الحساب فقط بواسطة المطور
@bot.message_handler(commands=['topup'])
def top_up(message):
    if message.from_user.username == developer_username:
        try:
            # حاول تحويل المدخلات إلى عدد صحيح (المبلغ الجديد)
            new_balance = int(message.text.split()[1])
            with connect_db() as conn:
                with conn.cursor() as cursor:
                    # تحديث الرصيد في قاعدة البيانات
                    cursor.execute("UPDATE user_balances SET balance = %s WHERE user_id = %s", (new_balance, message.from_user.id))
                    conn.commit()
            
            bot.reply_to(message, f"تم تحديث رصيد الحساب إلى: {new_balance}")
        except (IndexError, ValueError):
            bot.reply_to(message, "يرجى إدخال رصيد صالح بعد الأمر.")
    else:
        bot.reply_to(message, "فقط المطور يمكنه تحديث رصيد الحساب.")

# تابع لمعالجة الضغط على الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'top_up':
        bot.answer_callback_query(call.id, text="للتعبئة، استخدم الأمر التالي: /topup <المبلغ>")
    elif call.data == 'mobile_card':
        bot.answer_callback_query(call.id, text="تم اختيار كارت الهاتف.")
    elif call.data == 'game_card':
        bot.answer_callback_query(call.id, text="تم اختيار كارت شحن الألعاب.")
    elif call.data == 'app_card':
        bot.answer_callback_query(call.id, text="تم اختيار كارت التطبيقات.")
    elif call.data == 'balance':
        with connect_db() as conn:
            with conn.cursor() as cursor:
                # جلب الرصيد من قاعدة البيانات
                cursor.execute("SELECT balance FROM user_balances WHERE user_id = %s", (call.from_user.id,))
                result = cursor.fetchone()
                if result:
                    account_balance = result[0]
                else:
                    account_balance = 0

        bot.answer_callback_query(call.id, text=f"رصيد حسابك الحالي هو: {account_balance}")

# بدء البوت
bot.polling(non_stop=True)
