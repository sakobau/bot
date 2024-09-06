import telebot
from telebot import types

TOKEN = '7159716290:AAGTxMlWTfNZ9nI6dz0DbDanqP3TMw8u6SM
bot = telebot.TeleBot(TOKEN)

user_balances = {}
developer_username = 'm_55mg'
OWNER_USER_ID = 6649576561

def get_user_balance_markup(user):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    balance = user_balances.get(user, 0)
    btn_balance = types.KeyboardButton(f'الرصيد: {balance}')
    btn_asia = types.KeyboardButton('كارتات اسيا')
    btn_pubg = types.KeyboardButton('شدات ببجي')
    markup.add(btn_balance, btn_asia, btn_pubg)
    if user == developer_username:
        markup.add(types.KeyboardButton('شحن الرصيد'))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = get_user_balance_markup(message.from_user.username)
    bot.send_message(message.chat.id, "اختر من القائمة:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['كارتات اسيا', 'شدات ببجي'])
def handle_options(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if message.text == 'كارتات اسيا':
        values = ['5$', '10$', '20$']
        amounts = {'5$': 6000, '10$': 12000, '20$': 24000}
    else:
        values = ['360UC', '660UC']
        amounts = {'360UC': 8000, '660UC': 16000}
    
    for value in values:
        markup.add(types.KeyboardButton(value))
    markup.add(types.KeyboardButton('رجوع'))
    bot.send_message(message.chat.id, "اختر القيمة المطلوبة:" if message.text == 'كارتات اسيا' else "اختر عدد الشدات:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ['5$', '10$', '20$', '360UC', '660UC'])
def handle_purchase(message):
    amounts = {'5$': 6000, '10$': 12000, '20$': 24000, '360UC': 8000, '660UC': 16000}
    user = message.from_user.username
    if deduct_balance(user, amounts[message.text]):
        bot.send_message(message.chat.id, f"تم خصم {amounts[message.text]} من رصيدك.")
        if message.text in ['660UC']:
            order_details = f"طلب جديد:\nالاسم: {message.from_user.first_name}\nالمعرف: @{user}\nالطلب: {message.text}"
            bot.send_message(OWNER_USER_ID, order_details)
    else:
        bot.send_message(message.chat.id, "رصيدك غير كافٍ.")
    markup = get_user_balance_markup(user)
    bot.send_message(message.chat.id, "تم تحديث الرصيد:", reply_markup=markup)

def deduct_balance(user, amount):
    if user in user_balances and user_balances[user] >= amount:
        user_balances[user] -= amount
        return True
    return False

@bot.message_handler(func=lambda message: message.text == 'شحن الرصيد')
def add_balance_handler(message):
    if message.from_user.username == developer_username:
        bot.send_message(message.chat.id, "من فضلك أرسل المعرف الذي تريد شحنه والمبلغ بالصيغة التالية:\n@user 5000")
        bot.register_next_step_handler(message, process_add_balance)
    else:
        bot.send_message(message.chat.id, "غير مصرح لك باستخدام هذه الخاصية.")

def process_add_balance(message):
    if message.from_user.username == developer_username:
        try:
            user, amount = message.text.split()
            amount = int(amount)
            user = user.lstrip('@')
            if user not in user_balances:
                user_balances[user] = 0
            user_balances[user] += amount
            bot.send_message(message.chat.id, f"تم شحن {amount} لرصيد {user}. الرصيد الحالي هو: {user_balances[user]}")
            if message.chat.username == user:
                markup = get_user_balance_markup(user)
                bot.send_message(message.chat.id, "تم تحديث الرصيد:", reply_markup=markup)
        except:
            bot.send_message(message.chat.id, "حدث خطأ، يرجى التأكد من الصيغة وإعادة المحاولة.")
    else:
        bot.send_message(message.chat.id, "غير مصرح لك باستخدام هذه الخاصية.")

@bot.message_handler(func=lambda message: message.text == 'رجوع')
def back_handler(message):
    send_welcome(message)

bot.polling()
