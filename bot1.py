import telebot
from telebot import types

# توكن البوت الخاص بك
TOKEN = '8094828325:AAHkJ9Ej-drEH5AZctO6JzGNAEkAoM6SAOs'
bot = telebot.TeleBot(TOKEN)

# قيمة الرصيد
balance = 0

# دالة لعرض زر الرصيد
@bot.message_handler(commands=['start'])
def start(message):
    # إنشاء زر الرصيد
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    balance_button = types.KeyboardButton(f"الرصيد: {balance}")
    keyboard.add(balance_button)
    
    bot.send_message(message.chat.id, "مرحباً بك في بوت الرصيد!", reply_markup=keyboard)

# دالة لمعالجة الأزرار
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text.startswith("الرصيد:"):
        bot.send_message(message.chat.id, "هذا هو رصيدك الحالي: 0 لا يمكن الضغط عليه.")

bot.polling()
