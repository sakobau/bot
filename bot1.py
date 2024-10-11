import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توكن البوت الخاص بك
TOKEN = '7918486703:AAFlQxZtkKxENYRZ8T96ZZ1BW7Jo2ez88Yw'
OWNER_USERNAME = 'm_55mg'  # اسم المالك

bot = telebot.TeleBot(TOKEN)

# متغير الرصيد
balance = 0

# دالة لعرض زر "الرصيد"
def get_balance_markup():
    markup = InlineKeyboardMarkup()
    # الزر الخاص بالرصيد لا يمكن الضغط عليه
    balance_button = InlineKeyboardButton(f"الرصيد: {balance}", callback_data="balance", callback_game=False)
    markup.add(balance_button)
    return markup

# أمر البدء لعرض زر الرصيد
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = get_balance_markup()
    bot.send_message(message.chat.id, "مرحباً بك! هذه هي معلومات رصيدك:", reply_markup=markup)

# أمر المالك لشحن الرصيد
@bot.message_handler(commands=['charge'])
def charge_balance(message):
    global balance
    if message.from_user.username == OWNER_USERNAME:
        try:
            # شحن الرصيد الجديد بناءً على ما يدخله المالك
            new_balance = int(message.text.split()[1])  # يأخذ القيمة المدخلة بعد "/charge"
            balance = new_balance
            bot.send_message(message.chat.id, f"تم تحديث الرصيد إلى: {balance}")
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, "يرجى إدخال قيمة صحيحة بعد الأمر /charge")

        # تحديث الزر لكل المحادثات المفتوحة
        markup = get_balance_markup()
        bot.send_message(message.chat.id, "تم تحديث الرصيد", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "ليس لديك صلاحية لتحديث الرصيد.")

bot.polling()
