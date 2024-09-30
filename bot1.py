import telebot
import os

# استبدل بـ TOKEN الخاص بك
TOKEN = '8090786845:AAFwLA0VEVphRorM31fyY44iMyXXK1EO9c0'
bot = telebot.TeleBot(TOKEN)

# دالة لإرسال الموسيقى
@bot.message_handler(commands=['صوف'])
def send_song(message):
    # الحصول على اسم الأغنية بعد الأمر
    song_name = message.text.split(maxsplit=1)
    
    if len(song_name) > 1:
        song_name = song_name[1]  # استخدم اسم الأغنية
        file_path = f'songs/{song_name}.mp3'  # تحديد مسار الملف
        
        # تحقق مما إذا كان الملف موجودًا
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as song:
                bot.send_audio(chat_id=message.chat.id, audio=song)
        else:
            bot.send_message(chat_id=message.chat.id, text='عذراً، الأغنية غير موجودة.')
    else:
        bot.send_message(chat_id=message.chat.id, text='يرجى كتابة اسم الأغنية بعد الأمر "صوف".')

# بدء تشغيل البوت
bot.polling()
