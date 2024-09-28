import telebot
from telebot import types

# توكن البوت الذي حصلت عليه من BotFather
API_TOKEN = '7889761662:AAETDbWkCIX_sDXEQWai9LYeMkdg7NAtUoE'

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
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("هنا")
    add_button = types.KeyboardButton("اضف زر +")
    
    markup.add(button, add_button)

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# التعامل مع الرسائل النصية
@bot.message_handler(func=lambda message: message.text == "هنا")
def send_link(message):
    bot.send_message(message.chat.id, "رابط الاستفسارات: https://sakobau.github.io/inventory/")

# التعامل مع الضغط على زر "اضف زر +"
@bot.message_handler(func=lambda message: message.text == "اضف زر +")
def handle_add_button(message):
    user_states[message.from_user.id] = 'waiting_for_button_name'
    bot.send_message(message.chat.id, "الرجاء إدخال اسم الزر:")

# التعامل مع الرسائل النصية
@bot.message_handler(func=lambda message: message.from_user.id in user_states)
def handle_text(message):
    state = user_states[message.from_user.id]

    if state == 'waiting_for_button_name':
        if message.text.strip():  # تأكد من أن المدخل ليس فارغًا
            user_states[message.from_user.id] = 'waiting_for_button_content'
            user_states[message.from_user.id + "_button_name"] = message.text  # تخزين اسم الزر
            bot.send_message(message.chat.id, "الرجاء إدخال محتوى الزر:")
        else:
            bot.send_message(message.chat.id, "الاسم المدخل غير صالح، يرجى إدخال اسم زر صالح.")

    elif state == 'waiting_for_button_content':
        button_name = user_states.pop(message.from_user.id + "_button_name", None)
        if button_name:  # تحقق من وجود اسم الزر
            button_content = message.text  # الحصول على محتوى الزر
            user_states[message.from_user.id] = 'waiting_for_option'
            
            # إرسال تأكيد مع محتوى الزر
            bot.send_message(message.chat.id, f"تم إضافة زر '{button_name}' بمحتوى: '{button_content}'\nاختر من الخيارات التالية:")
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("صورة 🛡", "نـــــص 🖥")
            markup.add("سلعة ✨", "رابط 📟")
            markup.add("الرجوع")

            bot.send_message(message.chat.id, "اختر نوع الزر الذي تريد إضافته:", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "حدث خطأ، يرجى إعادة المحاولة.")

# التعامل مع خيارات الأزرار
@bot.message_handler(func=lambda message: message.text in ["صورة 🛡", "نـــــص 🖥", "سلعة ✨", "رابط 📟", "الرجوع"])
def handle_options(message):
    if message.text == "الرجوع":
        send_welcome(message)  # العودة للقائمة الرئيسية
        return
    
    # حسب الزر المحدد، اطلب من المستخدم إدخال البيانات المناسبة
    if message.text == "صورة 🛡":
        user_states[message.from_user.id] = 'waiting_for_image'
        bot.send_message(message.chat.id, "يرجى إرسال الصورة المطلوبة.")
    
    elif message.text == "نـــــص 🖥":
        user_states[message.from_user.id] = 'waiting_for_text'
        bot.send_message(message.chat.id, "يرجى إدخال النص المطلوب.")
    
    elif message.text == "سلعة ✨":
        user_states[message.from_user.id] = 'waiting_for_product'
        bot.send_message(message.chat.id, "يرجى إدخال سعر السلعة ووصفها.")
    
    elif message.text == "رابط 📟":
        user_states[message.from_user.id] = 'waiting_for_link'
        bot.send_message(message.chat.id, "يرجى إدخال وصف الرابط والرابط المطلوب.")

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
