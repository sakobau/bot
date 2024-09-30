import telebot
import os
import yt_dlp

# حط توكن البوت مالك هنا
TOKEN = '8090786845:AAFwLA0VEVphRorM31fyY44iMyXXK1EO9c0'
bot = telebot.TeleBot(TOKEN)

# دالة لتحميل الأغنية من يوتيوب
def download_song(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'songs/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# دالة لإرسال الموسيقى
@bot.message_handler(commands=['صوف'])
def send_song(message):
    # خذ الرابط من الرسالة
    url = message.text.split(maxsplit=1)

    if len(url) > 1:
        url = url[1]  # استخدم الرابط
        try:
            download_song(url)  # حاول تحميل الأغنية
            song_file = os.listdir('songs')[-1]  # خذ آخر ملف تم تحميله
            
            with open(f'songs/{song_file}', 'rb') as song:
                bot.send_audio(chat_id=message.chat.id, audio=song)
        except Exception as e:
            bot.send_message(chat_id=message.chat.id, text='عذراً، حصلت مشكلة في تحميل الأغنية.')
            print(e)
    else:
        bot.send_message(chat_id=message.chat.id, text='رجاءً اكتب رابط الأغنية بعد الأمر "صوف".')

# إنشاء مجلد لتخزين الأغاني إذا ما موجود
if not os.path.exists('songs'):
    os.makedirs('songs')

# بدء تشغيل البوت
bot.polling()
