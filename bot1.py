import telebot
from telebot import types

# ضع هنا الرمز الذي حصلت عليه من BotFather
TOKEN = '7159716290:AAGTxMlWTfNZ9nI6dz0DbDanqP3TMw8u6SM'
CHANNEL_USERNAME = '@rbi1001'  # اسم القناة مع علامة @
OWNER_USER_ID = 6649576561  # User ID الخاص بالمطور (الرسائل المحفوظة)

bot = telebot.TeleBot(TOKEN)

# متغير لتخزين الرصيد لكل مستخدم
user_balances = {}

# معرف المطور
developer_username = 'm_55mg'  # بدون علامة @ للتوافق مع الرسالة القادمة من تليجرام
developer_id = 6649576561  # معرف المستخدم الخاص بالمطور

# دالة للتحقق من اشتراك المستخدم في القناة
def is_user_subscribed(user_id):
    try:
        user_status = bot.get_chat_member(CHANNEL_USERNAME, user_id).status
        return user_status in ['member', 'administrator', 'creator']
    except Exception as e:
        return False

# دالة لإنشاء لوحة مفاتيح المستخدم
def get_user_balance_markup(user):
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

# ترحيب المستخدم
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not is_user_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn_subscribe = types.InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")
        markup.add(btn_subscribe)
        bot.send_message(message.chat.id, f"من فضلك اشترك في القناة {CHANNEL_USERNAME} لاستخدام البوت.", reply_markup=markup)
    else:
        markup = get_user_balance_markup(message.from_user.username)
        bot.send_message(message.chat.id, "اختر من القائمة:", reply_markup=markup)

# التعامل مع كارتات آسيا
@bot.message_handler(func=lambda message: message.text == 'كارتات اسيا')
def asia_cards_handler(message):
    if not is_user_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn_subscribe = types.InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")
        markup.add(btn_subscribe)
        bot.send_message(message.chat.id, f"من فضلك اشترك في القناة {CHANNEL_USERNAME} لاستخدام البوت.", reply_markup=markup)
        return
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_5dollars = types.KeyboardButton('5$')
    btn_10dollars = types.KeyboardButton('10$')
    btn_15dollars = types.KeyboardButton('15$')
    btn_20dollars = types.KeyboardButton('20$')
    btn_25dollars = types.KeyboardButton('25$')
    btn_back = types.KeyboardButton('رجوع')

    markup.add(btn_5dollars, btn_10dollars)
    markup.add(btn_15dollars, btn_20dollars)
    markup.add(btn_25dollars)
    markup.add(btn_back)
    
    bot.send_message(message.chat.id, "اختر القيمة المطلوبة:", reply_markup=markup)

# التعامل مع شدات ببجي
@bot.message_handler(func=lambda message: message.text == 'شدات ببجي')
def pubg_uc_handler(message):
    if not is_user_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        btn_subscribe = types.InlineKeyboardButton("اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")
        markup.add(btn_subscribe)
        bot.send_message(message.chat.id, f"من فضلك اشترك في القناة {CHANNEL_USERNAME} لاستخدام البوت.", reply_markup=markup)
        return
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_60uc = types.KeyboardButton('60UC')
    btn_360uc = types.KeyboardButton('360UC')
    btn_660uc = types.KeyboardButton('660UC')
    btn_720uc = types.KeyboardButton('720UC')
    btn_1950uc = types.KeyboardButton('1950UC')
    btn_back = types.KeyboardButton('رجوع')

    markup.add(btn_60uc, btn_360uc)
    markup.add(btn_660uc, btn_720uc)
    markup.add(btn_1950uc)
    markup.add(btn_back)

    bot.send_message(message.chat.id, "اختر القيمة المطلوبة:", reply_markup=markup)

# معالجة خصم الرصيد عند اختيار شدات ببجي
@bot.message_handler(func=lambda message: message.text in ['60UC', '360UC', '660UC', '720UC', '1950UC'])
def handle_pubg_uc_selection(message):
    price_map = {
        '60UC': 3000,
        '360UC': 8000,
        '660UC': 14000,
        '720UC': 16000,
        '1950UC': 35000
    }
    
    amount = price_map.get(message.text)
    if amount:
        ask_confirmation(message, amount)

# معالجة خصم الرصيد عند اختيار كارتات آسيا
@bot.message_handler(func=lambda message: message.text in ['5$', '10$', '15$', '20$', '25$'])
def handle_asia_card_selection(message):
    price_map = {
        '5$': 7000,
        '10$': 12000,
        '15$': 17000,
        '20$': 22000,
        '25$': 27000
    }
    
    amount = price_map.get(message.text)
    if amount:
        ask_confirmation(message, amount)

# العودة إلى القائمة الرئيسية
@bot.message_handler(func=lambda message: message.text == 'رجوع')
def handle_back(message):
    markup = get_user_balance_markup(message.from_user.username)
    bot.send_message(message.chat.id, "اختر من القائمة:", reply_markup=markup)

# تأكيد خصم الرصيد
def ask_confirmation(message, amount):
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton("نعم", callback_data=f"confirm_yes_{amount}")
    btn_no = types.InlineKeyboardButton("لا", callback_data="confirm_no")
    markup.add(btn_yes, btn_no)
    
    bot.send_message(message.chat.id, f"هل تريد استقطاع مبلغ {amount} من رصيدك؟", reply_markup=markup)

# تأكيد نعم لخصم الرصيد
@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_yes_'))
def confirm_yes(call):
    amount = int(call.data.split('_')[-1])
    user = call.from_user.username

    if deduct_balance(user, amount):
        bot.answer_callback_query(call.id, f"تم خصم {amount} من رصيدك.")
        bot.send_message(call.message.chat.id, f"تم استقطاع {amount} من رصيدك.")
    else:
        bot.answer_callback_query(call.id, "رصيدك غير كافٍ.")
        bot.send_message(call.message.chat.id, "رصيدك غير كافٍ.")
    
    markup = get_user_balance_markup(user)
    bot.send_message(call.message.chat.id, "تم تحديث الرصيد:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_no')
def confirm_no(call):
    bot.answer_callback_query(call.id, "تم إلغاء العملية.")
    bot.send_message(call.message.chat.id, "تم إلغاء العملية.")

# دالة خصم الرصيد
def deduct_balance(user, amount):
    if user in user_balances and user_balances[user] >= amount:
        user_balances[user] -= amount
        return True
    return False

# شحن الرصيد (للمطور فقط)
@bot.message_handler(func=lambda message: message.text == 'شحن الرصيد' and message.from_user.username == developer_username)
def ask_user_for_recharge(message):
    bot.send_message(message.chat.id, "الرجاء إرسال اسم المستخدم لشحن الرصيد.")

# استقبال اسم المستخدم لشحن الرصيد
@bot.message_handler(func=lambda message: message.from_user.username == developer_username and message.text.startswith('@'))
def ask_amount_for_recharge(message):
    username = message.text.lstrip('@')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    for amount in range(10000, 100001, 10000):
        markup.add(types.KeyboardButton(f'{amount}'))
    
    bot.send_message(message.chat.id, f"اختر المبلغ لشحن {username}:", reply_markup=markup)
    bot.register_next_step_handler(message, recharge_user, username)

# شحن المستخدم بالمبلغ المختار
def recharge_user(message, username):
    try:
        amount = int(message.text)
        if username in user_balances:
            user_balances[username] += amount
        else:
            user_balances[username] = amount
        bot.send_message(message.chat.id, f"تم شحن {amount} إلى {username}.")
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء اختيار مبلغ صالح.")

# بدء تشغيل البوت
bot.polling()
