import telebot
from telebot import types

# تعيين التوكن الخاص بالبوت
TOKEN = '8131016207:AAHC6QQIHw48c-XHCRQAYMOKk5PUu3n3vws'
bot = telebot.TeleBot(TOKEN)

# دالة معالجة الأمر /start
@bot.message_handler(commands=['start'])
def start(message):
    # قيمة رصيد الحساب (تبدأ من 0 ويمكن تعديلها من قبل المطور)
    account_balance = 0
    
    # إعداد الرسالة الترحيبية
    welcome_message = "مرحبا بك في متجر ســـــــــــوبر تــــــكنو للخدمات الالكترونية\nللاستفسار مراسلة المطور @m_55mg"

    # إعداد الأزرار الشفافة باستخدام InlineKeyboardMarkup
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # الأزرار
    button_1 = types.InlineKeyboardButton(text="تعبئة رصيد حسابي", callback_data='balance_fill')
    button_2 = types.InlineKeyboardButton(text="كارت هاتف", callback_data='phone_card')
    button_3 = types.InlineKeyboardButton(text="كارت شحن العاب", callback_data='game_card')
    button_4 = types.InlineKeyboardButton(text="كارت تطبيقات", callback_data='app_card')

    # إضافة الأزرار إلى الواجهة
    markup.add(button_1, button_2, button_3, button_4)

    # إرسال الرسالة الترحيبية مع الأزرار الشفافة
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

    # إرسال رسالة رصيد الحساب
    bot.send_message(message.chat.id, f"رصيد حسابي: {account_balance}", reply_markup=markup)

# معالجة الضغط على الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query_handler(call):
    if call.data == "balance_fill":
        bot.answer_callback_query(call.id, "أنت الآن في صفحة تعبئة الرصيد.")
    elif call.data == "phone_card":
        bot.answer_callback_query(call.id, "لقد اخترت كارت الهاتف.")
    elif call.data == "game_card":
        bot.answer_callback_query(call.id, "لقد اخترت كارت شحن الألعاب.")
    elif call.data == "app_card":
        bot.answer_callback_query(call.id, "لقد اخترت كارت التطبيقات.")

# تشغيل البوت
bot.polling(none_stop=True)
