import telebot
from telebot import types

# ضع هنا الرمز الذي حصلت عليه من BotFather
TOKEN = '7159716290:AAGTxMlWTfNZ9nI6dz0DbDanqP3TMw8u6SM'

bot = telebot.TeleBot(TOKEN)

# متغير لتخزين الرصيد
balance = 0

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # إنشاء لوحة المفاتيح المخصصة
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # إنشاء زر "كارتات اسيا"
    btn_asia = types.KeyboardButton('كارتات اسيا')
    
    # إضافة الزر إلى اللوحة
    markup.add(btn_asia)
    
    # إرسال رسالة مع اللوحة
    bot.send_message(message.chat.id, "اختر من القائمة:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'كارتات اسيا')
def asia_cards_handler(message):
    # إنشاء لوحة مفاتيح جديدة تحتوي على زر "5$" وزر "10$" وزر "رجوع"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    btn_5dollars = types.KeyboardButton('5$')
    btn_10dollars = types.KeyboardButton('10$')  # زر جديد
    btn_back = types.KeyboardButton('رجوع')
    
    # إضافة الأزرار إلى اللوحة
    markup.add(btn_5dollars)
    markup.add(btn_10dollars)  # إضافة الزر الجديد
    markup.add(btn_back)
    
    # إرسال رسالة مع اللوحة الجديدة
    bot.send_message(message.chat.id, "اختر القيمة المطلوبة:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '5$')
def five_dollars_handler(message):
    # إنشاء لوحة مفاتيح مدمجة تحتوي على أزرار "نعم" و "لا"
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('نعم', callback_data='confirm_yes_5')
    btn_no = types.InlineKeyboardButton('لا', callback_data='confirm_no')
    
    # إضافة الأزرار إلى اللوحة
    markup.add(btn_yes, btn_no)
    
    # إرسال رسالة مع اللوحة الجديدة
    bot.send_message(message.chat.id, "ستتم عملية الاستقطاع من الرصيد بمقدار 6000. هل أنت موافق؟", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == '10$')
def ten_dollars_handler(message):
    # إنشاء لوحة مفاتيح مدمجة تحتوي على أزرار "نعم" و "لا"
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('نعم', callback_data='confirm_yes_10')
    btn_no = types.InlineKeyboardButton('لا', callback_data='confirm_no')
    
    # إضافة الأزرار إلى اللوحة
    markup.add(btn_yes, btn_no)
    
    # إرسال رسالة مع اللوحة الجديدة
    bot.send_message(message.chat.id, "ستتم عملية الاستقطاع من الرصيد بمقدار 12000. هل أنت موافق؟", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_yes_5')
def confirm_yes_5(call):
    bot.answer_callback_query(call.id, text="سيتم إرسال معلوماتك إلى المجهز وسيتم تجهيزك بالرصيد بأقرب وقت ممكن.")
    # إرسال رسالة تأكيدية
    bot.send_message(call.message.chat.id, "شكراً لك! سيتم معالجة طلبك بأسرع وقت.")
    # العودة إلى القائمة الرئيسية بعد معالجة الطلب
    send_welcome(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_yes_10')
def confirm_yes_10(call):
    bot.answer_callback_query(call.id, text="سيتم إرسال معلوماتك إلى المجهز وسيتم تجهيزك بالرصيد بأقرب وقت ممكن.")
    # إرسال رسالة تأكيدية
    bot.send_message(call.message.chat.id, "شكراً لك! سيتم معالجة طلبك بأسرع وقت.")
    # العودة إلى القائمة الرئيسية بعد معالجة الطلب
    send_welcome(call.message)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_no')
def confirm_no(call):
    # إنشاء لوحة مفاتيح جديدة تحتوي على زر "رجوع"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton('رجوع')
    markup.add(btn_back)
    
    # إرسال رسالة مع اللوحة الجديدة
    bot.send_message(call.message.chat.id, "تم إلغاء العملية.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'رجوع')
def back_handler(message):
    # العودة إلى القائمة الرئيسية
    send_welcome(message)

# بدء تشغيل البوت
bot.polling()
