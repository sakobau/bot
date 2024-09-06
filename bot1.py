import telebot
from telebot import types

# ضع هنا الرمز الذي حصلت عليه من BotFather
TOKEN = '7159716290:AAGTxMlWTfNZ9nI6dz0DbDanqP3TMw8u6SM'
CHANNEL_USERNAME = '@arbi1001'  # اسم القناة مع علامة @
OWNER_USER_ID = 6649576561  # User ID الخاص بالمطور (الرسائل المحفوظة)

bot = telebot.TeleBot(TOKEN)

# متغير لتخزين الرصيد لكل مستخدم
user_balances = {}

# معرف المطور
developer_username = 'm_55mg'  # بدون علامة @ للتوافق مع الرسالة القادمة من تليجرام

def is_user_subscribed(user_id):
    """
    دالة للتحقق من اشتراك المستخدم في القناة.
    """
    try:
        user_status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return user_status in ['member', 'administrator', 'creator']
    except Exception as e:
        return False

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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # التحقق إذا كان المستخدم مشتركًا في القناة
    if not is_user_subscribed(message.from_user.id):
        # إرسال رسالة تطلب من المستخدم الاشتراك في القناة
        markup = types.InlineKeyboardMarkup()
        btn_subscribe = types.InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")
        markup.add(btn_subscribe)
        bot.send_message(message.chat.id, f"من فضلك اشترك في القناة {CHANNEL_USERNAME} لاستخدام البوت.", reply_markup=markup)
    else:
        # إرسال رسالة مع اللوحة المخصصة
        markup = get_user_balance_markup(message.from_user.username)
        bot.send_message(message.chat.id, "اختر من القائمة:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'كارتات اسيا')
def asia_cards_handler(message):
    if not is_user_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn_subscribe = types.InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")
        markup.add(btn_subscribe)
        bot.send_message(message.chat.id, f"من فضلك اشترك في القناة {CHANNEL_USERNAME} لاستخدام البوت.", reply_markup=markup)
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

@bot.message_handler(func=lambda message: message.text == 'شدات ببجي')
def pubg_handler(message):
    if not is_user_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn_subscribe = types.InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")
        markup.add(btn_subscribe)
        bot.send_message(message.chat.id, f"من فضلك اشترك في القناة {CHANNEL_USERNAME} لاستخدام البوت.", reply_markup=markup)
        return
    
    # إنشاء لوحة مفاتيح جديدة تحتوي على زر "360UC" وزر "660UC" وزر "رجوع"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn_360uc = types.KeyboardButton('360UC')  # زر 360UC
    btn_660uc = types.KeyboardButton('660UC')  # زر جديد 660UC
    btn_back = types.KeyboardButton('رجوع')
    
    # إضافة الأزرار إلى اللوحة
    markup.add(btn_360uc)
    markup.add(btn_660uc)  # إضافة الزر 660UC
    markup.add(btn_back)
    
    # إرسال رسالة مع اللوحة الجديدة
    bot.send_message(message.chat.id, "اختر عدد الشدات:", reply_markup=markup)

# دالة التأكيد
def ask_confirmation(message, amount):
    """
    عرض رسالة تأكيد للمستخدم لخصم مبلغ معين من رصيده.
    """
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("نعم", callback_data=f"confirm_yes_{amount}")
    btn_no = types.InlineKeyboardButton("لا", callback_data="confirm_no")
    markup.add(btn_yes, btn_no)
    
    bot.send_message(message.chat.id, f"هل تريد استقطاع مبلغ {amount} من رصيدك؟", reply_markup=markup)

# دوال لكل زر من الأزرار
@bot.message_handler(func=lambda message: message.text == '5$')
def five_dollars_handler(message):
    ask_confirmation(message, 7000)

@bot.message_handler(func=lambda message: message.text == '10$')
def ten_dollars_handler(message):
    ask_confirmation(message, 12000)

@bot.message_handler(func=lambda message: message.text == '20$')
def twenty_dollars_handler(message):
    ask_confirmation(message, 24000)

@bot.message_handler(func=lambda message: message.text == '360UC')
def uc_360_handler(message):
    ask_confirmation(message, 8000)

@bot.message_handler(func=lambda message: message.text == '660UC')
def uc_660_handler(message):
    ask_confirmation(message, 16000)

# ردود أزرار التأكيد
@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_yes_'))
def confirm_yes(call):
    # استخراج المبلغ من الـ callback data
    amount = int(call.data.split('_')[-1])
    user = call.from_user.username
    
    # خصم الرصيد
    if deduct_balance(user, amount):
        bot.answer_callback_query(call.id, f"تم خصم {amount} من رصيدك.")
        bot.send_message(call.message.chat.id, f"تم استقطاع {amount} من رصيدك.")
    else:
        bot.answer_callback_query(call.id, "رصيدك غير كافٍ.")
        bot.send_message(call.message.chat.id, "رصيدك غير كافٍ.")
    
    # تحديث لوحة المفاتيح
    markup = get_user_balance_markup(user)
    bot.send_message(call.message.chat.id, "تم تحديث الرصيد:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_no')
def confirm_no(call):
    # إلغاء العملية
    bot.answer_callback_query(call.id, "تم إلغاء العملية.")
    bot.send_message(call.message.chat.id, "تم إلغاء العملية.")

def deduct_balance(user, amount):
    """
    دالة لخصم الرصيد من المستخدم.
    """
    if user in user_balances and user_balances[user] >= amount:
        user_balances[user] -= amount
        return True
    return False

# بدء تشغيل البوت
bot.polling()
