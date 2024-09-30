import telebot
from telebot import types

# حط توكن البوت مالك هنا
TOKEN = 'YOUR_BOT_TOKEN'
bot = telebot.TeleBot(TOKEN)

# دالة للترحيب بالمستخدمين الجدد
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "أهلاً بك في بوت وعد! كيف يمكنني مساعدتك اليوم؟")

# دالة لإجراء استطلاع
@bot.message_handler(commands=['استطلاع'])
def poll(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add('نعم', 'لا')
    msg = bot.send_message(message.chat.id, "هل تحب البوت؟", reply_markup=markup)
    bot.register_next_step_handler(msg, process_poll_response)

def process_poll_response(message):
    if message.text == 'نعم':
        bot.send_message(message.chat.id, "شكرًا لك!")
    else:
        bot.send_message(message.chat.id, "نأسف لأنك لا تحب البوت!")

# دالة لإرسال معلومات
@bot.message_handler(commands=['معلومات'])
def info(message):
    bot.send_message(message.chat.id, "هذا بوت بسيط يوفر لك بعض الميزات الأساسية. استخدم الأوامر التالية:\n/start - للترحيب\n/استطلاع - لإجراء استطلاع\n/معلومات - لمعرفة المزيد عن البوت")

# دالة لإدارة القناة
@bot.message_handler(commands=['إدارة'])
def manage_channel(message):
    bot.send_message(message.chat.id, "هذه ميزة إدارة القناة! يمكنك إضافة المزيد من الميزات هنا.")

# بدء تشغيل البوت
bot.polling()
