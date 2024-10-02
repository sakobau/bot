import telebot
import json
import os

# توكن البوت
bot = telebot.TeleBot('7500408322:AAHy2I93ZciXOyZ4EpU9jk1HpmJgGtBa2dQ')

# ملف قاعدة البيانات
users_file = 'users_db.json'

# تحميل قاعدة البيانات إذا كانت موجودة
if os.path.exists(users_file):
    with open(users_file, 'r') as f:
        users_db = json.load(f)
else:
    users_db = {}

# أمر التسجيل
@bot.message_handler(commands=['register'])
def register_user(message):
    try:
        username = message.from_user.username
        user_id = message.from_user.id
        
        # تخزين المستخدم في قاعدة البيانات
        users_db[username] = user_id
        
        # حفظ البيانات في الملف
        with open(users_file, 'w') as f:
            json.dump(users_db, f)
        
        bot.send_message(user_id, f"تم تسجيلك بنجاح، معرفك هو: {user_id}")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء التسجيل: {e}")

# استلام البيانات من Google Forms
@bot.message_handler(commands=['send_form_data'])
def handle_message(message):
    try:
        # استلام الرسالة على شكل JSON
        data = json.loads(message.text)
        
        # استخراج اسم المستخدم والبيانات
        username = data['username']
        form_data = data['formData']
        
        # البحث عن المستخدم المطلوب بناءً على الاسم
        user_id = users_db.get(username)
        
        if user_id:
            # إرسال البيانات إلى المستخدم المناسب
            bot.send_message(user_id, f"تم استلام البيانات:\n{form_data}")
        else:
            bot.send_message(message.chat.id, "لم يتم العثور على المستخدم. يجب أن يسجل المستخدم عبر البوت.")
    
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ: {e}")

# استلام الرسائل من المجموعة
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"معرف المجموعة هو: {message.chat.id}")

# بدء البوت
bot.polling()
