import telebot

# توكن البوت
TOKEN = "8094828325:AAHkJ9Ej-drEH5AZctO6JzGNAEkAoM6SAOs"
bot = telebot.TeleBot(TOKEN)

# عند استلام رسالة نصية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! كيف أستطيع مساعدتك؟")

# عند استلام رسالة عادية
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

# تشغيل البوت
bot.polling()
