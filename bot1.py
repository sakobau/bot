import telebot
from telebot import types

# حط توكن البوت مالك هنا
TOKEN = '8090786845:AAFwLA0VEVphRorM31fyY44iMyXXK1EO9c0'
bot = telebot.TeleBot(TOKEN)

# دالة للترحيب بالمستخدمين الجدد
@bot.message_handler(commands=['start'])
def welcome(message):
    # إنشاء زر شفاف
    markup = types.InlineKeyboardMarkup()
    add_button = types.InlineKeyboardButton("اضفني للمجموعة 🔥🖥", url="https://t.me/D7Bot?startgroup=Commands&admin=ban_users+restrict_members+delete_messages+add_admins+change_info+invite_users+pin_messages+manage_call+manage_chat+manage_video_chats+promote_members")
    markup.add(add_button)
    
    bot.send_message(
        message.chat.id,
        "أهلاً بك في بوت وعد! كيف يمكنني مساعدتك اليوم؟",
        reply_markup=markup
    )

# دالة لتفعيل البوت
@bot.message_handler(func=lambda message: message.text.lower() == 'تفعيل')
def activate_bot(message):
    # تأكد أن المستخدم لديه صلاحيات الإدارة في المجموعة
    if message.from_user.id in [admin.user.id for admin in bot.get_chat_administrators(message.chat.id)]:
        bot.send_message(message.chat.id, "تم تفعيل البوت بنجاح في المجموعة!")
    else:
        bot.send_message(message.chat.id, "عذراً، تحتاج إلى صلاحيات الإدارة لتفعيل البوت.")

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
    bot.send_message(message.chat.id, "هذا بوت بسيط يوفر لك بعض الميزات الأساسية. استخدم الأوامر التالية:\n/start - للترحيب\n/استطلاع - لإجراء استطلاع\nاكتب 'تفعيل' لتفعيل البوت\n/معلومات - لمعرفة المزيد عن البوت")

# دالة لإدارة القناة
@bot.message_handler(commands=['إدارة'])
def manage_channel(message):
    bot.send_message(message.chat.id, "هذه ميزة إدارة القناة! يمكنك إضافة المزيد من الميزات هنا.")

# بدء تشغيل البوت
bot.polling()
