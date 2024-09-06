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

@bot.message_handler(func=lambda message: message.text == 'شحن الرصيد')
def add_balance_handler(message):
    if message.from_user.username != developer_username:
        bot.send_message(message.chat.id, "هذا الزر مخصص للمطور فقط.")
        return
    
    bot.send_message(message.chat.id, "أرسل الآن اسم المستخدم الذي تريد شحن رصيده.")
    bot.register_next_step_handler(message, process_user_for_balance)

def process_user_for_balance(message):
    global target_user
    
    target_user = message.text.strip()  # تخزين اسم المستخدم للمستخدم الذي سيتم شحن رصيده
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    amounts = ['10000', '20000', '30000', '40000', '50000', '60000', '70000', '80000', '90000', '100000']
    
    for amount in amounts:
        markup.add(types.KeyboardButton(f'{amount}'))
    btn_back = types.KeyboardButton('رجوع')
    markup.add(btn_back)
    
    bot.send_message(message.chat.id, "اختر المبلغ الذي تريد شحنه:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.isdigit() and int(message.text) in range(10000, 100001))
def handle_amount_selection(message):
    global target_user
    
    amount = int(message.text)
    
    if target_user in user_balances:
        user_balances[target_user] += amount
    else:
        user_balances[target_user] = amount
    
    bot.send_message(message.chat.id, f"تم شحن {amount} إلى رصيد {target_user}.")
    
    # تحديث لوحة المفاتيح للمطور
    markup = get_user_balance_markup(developer_username)
    bot.send_message(message.chat.id, "تم تحديث الرصيد:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'رجوع')
def handle_back(message):
    markup = get_user_balance_markup(developer_username)
    bot.send_message(message.chat.id, "اختر من القائمة:", reply_markup=markup)

# ... باقي الشيفرة كما هي

bot.polling()
