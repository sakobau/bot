import telebot
from telebot import types

# توكن البوت الذي حصلت عليه من BotFather
API_TOKEN = 'YOUR_BOT_TOKEN'

# اسم المستخدم الخاص بالمطور
DEVELOPER_USERNAME = 'm_55mg'

# إنشاء كائن البوت
bot = telebot.TeleBot(API_TOKEN)

# متغير لتخزين الحالة الحالية للمستخدم
user_states = {}

# التعامل مع الرسائل التي تحتوي على أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "هذا البوت مبرمج من المطور مصطفى الاسدي و يوزره @m_55mg\n"
        "يمكنه برمجة تطبيقات و بوتات، يرجى ارسال استفسارك "
    )
    
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("هنا", url="https://sakobau.github.io/inventory/")
    add_button = types.InlineKeyboardButton("اضف زر +", callback_data="add_button")
    
    markup.add(button, add_button)

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# التعامل مع الضغط على زر "اضف زر +"
@bot.callback_query_handler(func=lambda call: call.data == "add_button")
def handle_add_button(call):
    user_states[call.from_user.id] = 'waiting_for_button_name'
    bot.answer_callback_query(call.id, "الرجاء إدخال اسم الزر:")
    bot.send_message(call.message.chat.id, "الرجاء إدخال اسم الزر:")

# التعامل مع الرسائل النصية
@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def handle_text(message):
    state = user_states[message.from_user.id]

    if state == 'waiting_for_button_name':
        user_states[message.from_user.id] = 'waiting_for_button_content'
        user_states[message.from_user.id + "_button_name"] = message.text  # تخزين اسم الزر
        bot.send_message(message.chat.id, "الرجاء إدخال محتوى الزر:")
    
    elif state == 'waiting_for_button_content':
        button_name = user_states.pop(message.from_user.id + "_button_name", None)
        user_states[message.from_user.id] = 'waiting_for_option'
        bot.send_message(message.chat.id, f"تم إضافة زر '{button_name}' بمحتوى: {message.text}\nاختر من الخيارات التالية:")
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("صورة 🛡", callback_data="add_image"))
        markup.add(types.InlineKeyboardButton("نـــــص 🖥", callback_data="add_text"))
        markup.add(types.InlineKeyboardButton("سلعة ✨", callback_data="add_product"))
        markup.add(types.InlineKeyboardButton("رابط 📟", callback_data="add_link"))
        markup.add(types.InlineKeyboardButton("الرجوع", callback_data="go_back"))

        bot.send_message(message.chat.id, "اختر نوع الزر الذي تريد إضافته:", reply_markup=markup)

# التعامل مع خيارات الأزرار
@bot.callback_query_handler(func=lambda call: call.data in ["add_image", "add_text", "add_product", "add_link", "go_back"])
def handle_options(call):
    if call.data == "go_back":
        send_welcome(call.message)  # العودة للقائمة الرئيسية
        return
    
    # حسب الزر المحدد، اطلب من المستخدم إدخال البيانات المناسبة
    if call.data == "add_image":
        user_states[call.from_user.id] = 'waiting_for_image'
        bot.answer_callback_query(call.id, "يرجى إرسال الصورة المطلوبة.")
    
    elif call.data == "add_text":
        user_states[call.from_user.id] = 'waiting_for_text'
        bot.answer_callback_query(call.id, "يرجى إدخال النص المطلوب.")
    
    elif call.data == "add_product":
        user_states[call.from_user.id] = 'waiting_for_product'
        bot.answer_callback_query(call.id, "يرجى إدخال سعر السلعة ووصفها.")
    
    elif call.data == "add_link":
        user_states[call.from_user.id] = 'waiting_for_link'
        bot.answer_callback_query(call.id, "يرجى إدخال وصف الرابط والرابط المطلوب.")

# التعامل مع الرسائل حسب حالة المستخدم
@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def handle_dynamic_inputs(message):
    state = user_states[message.from_user.id]

    if state == 'waiting_for_image':
        # هنا يمكنك معالجة الصورة المرسلة
        bot.send_message(message.chat.id, "تم استلام الصورة.")
        user_states.pop(message.from_user.id)  # إزالة الحالة
    
    elif state == 'waiting_for_text':
        bot.send_message(message.chat.id, f"تم استلام النص: {message.text}")
        user_states.pop(message.from_user.id)  # إزالة الحالة
    
    elif state == 'waiting_for_product':
        bot.send_message(message.chat.id, f"تم استلام المنتج: {message.text}")
        user_states.pop(message.from_user.id)  # إزالة الحالة

    elif state == 'waiting_for_link':
        bot.send_message(message.chat.id, f"تم استلام الرابط: {message.text}")
        user_states.pop(message.from_user.id)  # إزالة الحالة

# تشغيل البوت في وضع الاستماع
bot.polling()
