import telebot
from telebot import types

# أدخل مفتاح API الخاص بالبوت هنا
API_TOKEN = "8090786845:AAFwLA0VEVphRorM31fyY44iMyXXK1EO9c0"
bot = telebot.TeleBot(API_TOKEN)

# تابع لتنفيذ الأمر /start عند الضغط عليه
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    
    # إعداد الرصيد (يمكن تعديله لاحقًا)
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
        bot.answer_callback_query(call.id, text=f"رصيدك الحالي هو: 0")

# بدء البوت
bot.polling(non_stop=True)
