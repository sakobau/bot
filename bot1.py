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

# دالة لخصم الرصيد وإرسال الطلب للمالك
def deduct_balance_and_notify(user, amount, order_description, chat_id):
    """
    دالة لخصم الرصيد من المستخدم وإرسال الطلب للمالك.
    """
    if user in user_balances and user_balances[user] >= amount:
        # خصم الرصيد
        user_balances[user] -= amount
        bot.send_message(chat_id, f"تم خصم {amount} من رصيدك مقابل {order_description}.")

        # إرسال الطلب إلى المالك
        order_details = f"طلب جديد:\nالاسم: {user}\nالطلب: {order_description}\nالمبلغ: {amount}"
        bot.send_message(OWNER_USER_ID, order_details)
        
        return True
    else:
        bot.send_message(chat_id, "رصيدك غير كافٍ.")
        return False

# التعامل مع شراء بطاقة 5$
@bot.message_handler(func=lambda message: message.text == '5$')
def five_dollars_handler(message):
    user = message.from_user.username
    if deduct_balance_and_notify(user, 7000, "بطاقة 5$", message.chat.id):
        bot.send_message(message.chat.id, "تم تقديم طلبك بنجاح.")

# التعامل مع شراء بطاقة 10$
@bot.message_handler(func=lambda message: message.text == '10$')
def ten_dollars_handler(message):
    user = message.from_user.username
    if deduct_balance_and_notify(user, 12000, "بطاقة 10$", message.chat.id):
        bot.send_message(message.chat.id, "تم تقديم طلبك بنجاح.")

# التعامل مع شراء بطاقة 20$
@bot.message_handler(func=lambda message: message.text == '20$')
def twenty_dollars_handler(message):
    user = message.from_user.username
    if deduct_balance_and_notify(user, 24000, "بطاقة 20$", message.chat.id):
        bot.send_message(message.chat.id, "تم تقديم طلبك بنجاح.")

# التعامل مع شراء شدات 360UC
@bot.message_handler(func=lambda message: message.text == '360UC')
def uc_360_handler(message):
    user = message.from_user.username
    if deduct_balance_and_notify(user, 8000, "360UC", message.chat.id):
        bot.send_message(message.chat.id, "تم تقديم طلبك بنجاح.")

# التعامل مع شراء شدات 660UC
@bot.message_handler(func=lambda message: message.text == '660UC')
def uc_660_handler(message):
    user = message.from_user.username
    if deduct_balance_and_notify(user, 16000, "660UC", message.chat.id):
        bot.send_message(message.chat.id, "تم تقديم طلبك بنجاح.")

# دالة شحن الرصيد للمطور فقط
@bot.message_handler(func=lambda message: message.text == 'شحن الرصيد')
def add_balance_handler(message):
    # التحقق إذا كان المستخدم هو المطور
    if message.from_user.username == developer_username:
        bot.send_message(message.chat.id, "من فضلك أرسل الايدي أو اليوزر الذي تريد شحنه.")
        bot.register_next_step_handler(message, process_user_for_balance)
    else:
        bot.send_message(message.chat.id, "غير مصرح لك باستخدام هذه الخاصية.")

# دالة لمعالجة الايدي أو اليوزر المدخل من المطور
def process_user_for_balance(message):
    user_identifier = message.text.strip()
    
    # حفظ اليوزر أو الايدي مؤقتًا لجلسة الشحن
    message.chat.current_user_for_balance = user_identifier
    
    # عرض الأزرار الشفافة للمبالغ
    markup = types.InlineKeyboardMarkup()
    
    # إنشاء أزرار بالمبالغ من 10000 إلى 100000
    amounts = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
    for amount in amounts:
        markup.add(types.InlineKeyboardButton(f"{amount}", callback_data=f"add_balance_{user_identifier}_{amount}"))
    
    bot.send_message(message.chat.id, "اختر المبلغ الذي تريد شحنه:", reply_markup=markup)

# رد على أزرار المبالغ
@bot.callback_query_handler(func=lambda call: call.data.startswith('add_balance_'))
def confirm_add_balance(call):
    # استخراج المعلومات من callback_data
    _, user_identifier, amount = call.data.split('_')
    amount = int(amount)
    
    # التحقق من وجود المستخدم في الرصيد، وإضافته إن لم يكن موجودًا
    if user_identifier not in user_balances:
        user_balances[user_identifier] = 0
    
    # إضافة المبلغ للرصيد
    user_balances[user_identifier] += amount
    
    # إرسال رسالة تأكيد للمطور
    bot.answer_callback_query(call.id, f"تم شحن {amount} لرصيد {user_identifier}.")
    bot.send_message(call.message.chat.id, f"تم شحن {amount} لرصيد {user_identifier}. الرصيد الحالي: {user_balances[user_identifier]}")

    # إرسال رسالة للمستخدم المستهدف إن كان موجودًا في المحادثة
    if call.message.chat.username == user_identifier:
        markup = get_user_balance_markup(user_identifier)
        bot.send_message(call.message.chat.id, "تم تحديث الرصيد:", reply_markup=markup)

# بدء تشغيل البوت
bot.polling()
