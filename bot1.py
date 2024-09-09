import telebot
from telebot import types

# ضع هنا الرمز الذي حصلت عليه من BotFather
TOKEN = '7242581979:AAGq_4IqGxPHsVdtp2ikeoYLwm0wwZawzz0'
CHANNEL_USERNAME = '@arbi1001'  # اسم القناة مع علامة @
OWNER_USER_ID = 6649576561  # User ID الخاص بالمطور

bot = telebot.TeleBot(TOKEN)

# متغير لتخزين الرصيد لكل مستخدم
user_balances = {}

# معرف المطور
developer_username = 'your_developer_username'  # بدون علامة @
developer_id = OWNER_USER_ID  # معرف المستخدم الخاص بالمطور

# متغير لتخزين الأزرار المضافة
custom_buttons = {}

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
        btn_add_balance = types.KeyboardButton('شحن الرصيد')
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

# دالة لإضافة زر جديد فقط للمطور
@bot.message_handler(func=lambda message: message.text == 'إضافة الأزرار' and message.from_user.username == developer_username)
def ask_button_name(message):
    bot.send_message(message.chat.id, "الرجاء إدخال اسم الزر الجديد:")
    bot.register_next_step_handler(message, add_custom_button)

def add_custom_button(message):
    button_name = message.text
    custom_buttons[button_name] = {}
    bot.send_message(message.chat.id, f"تم إضافة الزر: {button_name}. الآن يمكن للمطور إضافة أزرار داخل هذا الزر.")
    update_keyboards()

# دالة لإضافة أزرار داخل الزر الرئيسي مع سعر
@bot.message_handler(func=lambda message: message.text in custom_buttons and message.from_user.username == developer_username)
def ask_inner_button_name(message):
    parent_button = message.text
    bot.send_message(message.chat.id, f"أدخل اسم الزر الداخلي الذي ترغب بإضافته إلى {parent_button}:")
    bot.register_next_step_handler(message, ask_inner_button_price, parent_button)

def ask_inner_button_price(message, parent_button):
    inner_button_name = message.text
    bot.send_message(message.chat.id, f"أدخل سعر الزر {inner_button_name}:")
    bot.register_next_step_handler(message, add_inner_button, parent_button, inner_button_name)

def add_inner_button(message, parent_button, inner_button_name):
    try:
        price = int(message.text)
        custom_buttons[parent_button][inner_button_name] = price
        bot.send_message(message.chat.id, f"تم إضافة الزر {inner_button_name} بسعر {price} إلى {parent_button}.")
        update_keyboards()
    except ValueError:
        bot.send_message(message.chat.id, "الرجاء إدخال رقم صحيح للسعر.")

# دالة لتحديث لوحة المفاتيح لجميع المستخدمين والمطور
def update_keyboards():
    for user in user_balances:
        markup = get_user_balance_markup(user)
        for custom_button in custom_buttons:
            markup.add(types.KeyboardButton(custom_button))
        bot.send_message(user, "تم تحديث القائمة:", reply_markup=markup)

# معالجة اختيار الأزرار المخصصة
@bot.message_handler(func=lambda message: message.text in custom_buttons)
def handle_custom_button(message):
    parent_button = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    for inner_button, price in custom_buttons[parent_button].items():
        markup.add(types.KeyboardButton(f"{inner_button} - {price}"))
    markup.add(types.KeyboardButton('رجوع'))
    
    bot.send_message(message.chat.id, f"اختر زرًا من {parent_button}:", reply_markup=markup)

# خصم الرصيد عند اختيار الأزرار الداخلية
@bot.message_handler(func=lambda message: any(f"{btn} - " in message.text for btn in custom_buttons))
def handle_inner_custom_button(message):
    for parent_button, inner_buttons in custom_buttons.items():
        for inner_button, price in inner_buttons.items():
            if f"{inner_button} - {price}" == message.text:
                ask_confirmation(message, price)
                return

# دالة تأكيد خصم الرصيد
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
