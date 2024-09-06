import telebot
from telebot import types

# ضع هنا الرمز الذي حصلت عليه من BotFather
TOKEN = '7159716290:AAGTxMlWTfNZ9nI6dz0DbDanqP3TMw8u6SM'

bot = telebot.TeleBot(TOKEN)

# متغير لتخزين الرصيد لكل مستخدم
user_balances = {}

# معرف المطور
developer_username = 'm_55mg'  # بدون علامة @ للتوافق مع الرسالة القادمة من تليجرام
OWNER_USER_ID = 6649576561  # User ID الخاص بالمطور (الرسائل المحفوظة)

# قناة الاشتراك الإجباري
required_channel = '@arbi1001'  # ضع معرف القناة هنا

def get_user_balance_markup(user):
    """
    دالة لإنشاء لوحة المفاتيح مع زر الرصيد المحدث بناءً على رصيد المستخدم.
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    balance = user_balances.get(user, 0)
    btn_balance = types.KeyboardButton(f'الرصيد: {balance}')
    btn_asia = types.KeyboardButton('كارتات اسيا')
    btn_pubg = types.KeyboardButton('شدات ببجي')

    markup.add(btn_balance)
    markup.add(btn_asia, btn_pubg)
    
    if user == developer_username:
        btn_add_balance = types.KeyboardButton('شحن الرصيد')  # زر للمطور لشحن الرصيد
        markup.add(btn_add_balance)
    
    return markup

def is_user_subscribed(user_id):
    """
    دالة للتحقق مما إذا كان المستخدم مشتركًا في القناة المطلوبة.
    """
    try:
        member = bot.get_chat_member(required_channel, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # تحقق مما إذا كان المستخدم مشتركًا في القناة المطلوبة
    if not is_user_subscribed(message.from_user.id):
        # إرسال رسالة تطلب الاشتراك
        bot.send_message(message.chat.id, 
                         "🚸| عذرا عزيزي..\n🔰| عليك الاشتراك بقناة البوت لتتمكن من استخدامه\n\n"
                         "- https://t.me/arbi1001\n\n"
                         "‼️| اشترك ثم ارسل /start")
        return

    # إرسال رسالة مع اللوحة المخصصة إذا كان مشتركًا
    markup = get_user_balance_markup(message.from_user.username)
    bot.send_message(message.chat.id, "اختر من القائمة:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'كارتات اسيا')
def asia_cards_handler(message):
    # تحقق مما إذا كان المستخدم مشتركًا في القناة المطلوبة
    if not is_user_subscribed(message.from_user.id):
        # إرسال رسالة تطلب الاشتراك
        bot.send_message(message.chat.id, 
                         "🚸| عذرا عزيزي..\n🔰| عليك الاشتراك بقناة البوت لتتمكن من استخدامه\n\n"
                         "- https://t.me/arbi1001\n\n"
                         "‼️| اشترك ثم ارسل /start")
        return

    # إنشاء لوحة مفاتيح جديدة تحتوي على زر "5$" وزر "10$" وزر "20$" وزر "رجوع"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn_5dollars = types.KeyboardButton('5$')
    btn_10dollars = types.KeyboardButton('10$')  # زر 10$
    btn_20dollars = types.KeyboardButton('20$')  # زر جديد 20$
    btn_back = types.KeyboardButton('رجوع')
    
    # إضافة الأزرار إلى اللوحة
    markup.add(btn_5dollars)
    markup.add(btn_10dollars)  # إضافة الزر 10$
    markup.add(btn_20dollars)  # إضافة الزر الجديد 20$
    markup.add(btn_back)
    
    # إرسال رسالة مع اللوحة الجديدة
    bot.send_message(message.chat.id, "اختر القيمة المطلوبة:", reply_markup=markup)

# باقي الكود دون تغيير

# بدء تشغيل البوت
bot.polling()
