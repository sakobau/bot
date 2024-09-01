import telebot
from telebot import types

# ضع هنا الرمز الذي حصلت عليه من BotFather
TOKEN = '7159716290:AAGTxMlWTfNZ9nI6dz0DbDanqP3TMw8u6SM'

bot = telebot.TeleBot(TOKEN)

# متغير لتخزين الرصيد لكل مستخدم
user_balances = {}

# معرف المطور
developer_username = 'm_55mg'  # بدون علامة @ للتوافق مع الرسالة القادمة من تليجرام

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # إنشاء لوحة المفاتيح المخصصة
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # زر "الرصيد" كزر غير تفاعلي (كمثال الرقم 0، يمكن تحديثه لاحقاً)
    btn_balance = types.KeyboardButton('الرصيد: 0')

    # إنشاء زر "كارتات اسيا" وزر "شدات ببجي"
    btn_asia = types.KeyboardButton('كارتات اسيا')
    btn_pubg = types.KeyboardButton('شدات ببجي')

    # التحقق من إذا كان المستخدم هو المطور لإضافة زر "شحن الرصيد"
    if message.from_user.username == developer_username:
        btn_add_balance = types.KeyboardButton('شحن الرصيد')  # زر للمطور لشحن الرصيد
        markup.add(btn_add_balance)

    # إضافة الأزرار إلى اللوحة
    markup.add(btn_balance)
    markup.add(btn_asia)
    markup.add(btn_pubg)

    # إرسال رسالة مع اللوحة
    bot.send_message(message.chat.id, "اختر من القائمة:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'كارتات اسيا')
def asia_cards_handler(message):
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
    # تنفيذ بعض الإجراءات الخاصة بزر "شدات ببجي"
    bot.send_message(message.chat.id, "سيتم تنفيذ الإجراءات المطلوبة لشدات ببجي هنا.")

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

@bot.message_handler(func=lambda message: message.text == '20$')
def twenty_dollars_handler(message):
    # إنشاء لوحة مفاتيح مدمجة تحتوي على أزرار "نعم" و "لا"
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('نعم', callback_data='confirm_yes_20')
    btn_no = types.InlineKeyboardButton('لا', callback_data='confirm_no')
    
    # إضافة الأزرار إلى اللوحة
    markup.add(btn_yes, btn_no)
    
    # إرسال رسالة مع اللوحة الجديدة
    bot.send_message(message.chat.id, "ستتم عملية الاستقطاع من الرصيد بمقدار 24000. هل أنت موافق؟", reply_markup=markup)

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
            # استخراج المعرف والمبلغ من الرسالة
            user, amount = message.text.split()
            amount = int(amount)
            
            # تحديث الرصيد للمستخدم المحدد
            if user not in user_balances:
                user_balances[user] = 0
            user_balances[user] += amount
            
            # تحديث زر الرصيد
            bot.send_message(message.chat.id, f"تم شحن {amount} لرصيد {user}. الرصيد الحالي هو: {user_balances[user]}")
        except Exception as e:
            bot.send_message(message.chat.id, "حدث خطأ، يرجى التأكد من الصيغة وإعادة المحاولة.")
    else:
        bot.send_message(message.chat.id, "غير مصرح لك باستخدام هذه الخاصية.")

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

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_yes_20')
def confirm_yes_20(call):
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
