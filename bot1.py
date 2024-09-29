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
    
    # إنشاء لوحة الأزرار
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_1 = types.KeyboardButton("تعبئة رصيد حسابي")
    button_2 = types.KeyboardButton("كارت هاتف")
    button_3 = types.KeyboardButton("كارت شحن العاب")
    button_4 = types.KeyboardButton("كارت تطبيقات")
    
    markup.add(button_1, button_2, button_3, button_4)

    # إرسال الرسالة الترحيبية مع لوحة الأزرار
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

    # إرسال زر "رصيد حسابي" في الأعلى
    bot.send_message(message.chat.id, f"رصيد حسابي: {account_balance}", reply_markup=markup)

# دالة معالجة الرسائل
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "تعبئة رصيد حسابي":
        bot.send_message(message.chat.id, "أنت الآن في صفحة تعبئة الرصيد.")
    elif message.text == "كارت هاتف":
        bot.send_message(message.chat.id, "لقد اخترت كارت الهاتف.")
    elif message.text == "كارت شحن العاب":
        bot.send_message(message.chat.id, "لقد اخترت كارت شحن الألعاب.")
    elif message.text == "كارت تطبيقات":
        bot.send_message(message.chat.id, "لقد اخترت كارت التطبيقات.")

# تشغيل البوت
bot.polling(none_stop=True)
