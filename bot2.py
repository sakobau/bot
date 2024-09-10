from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# المتغيرات لتخزين معلومات المستخدم
user_data = {}

# دالة البدء
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("أهلاً! الرجاء إدخال اسم العميل.")

# استقبال اسم العميل
def get_name(update: Update, context: CallbackContext) -> None:
    user_data['name'] = update.message.text
    update.message.reply_text(f"تم استلام الاسم: {user_data['name']}\nالرجاء إدخال المنتجات.")

# استقبال تفاصيل الفاتورة
def get_products(update: Update, context: CallbackContext) -> None:
    user_data['products'] = update.message.text
    update.message.reply_text(f"تم استلام المنتجات: {user_data['products']}\nالرجاء إدخال السعر.")

# استقبال السعر وتحويل المعلومات إلى فاتورة
def get_price(update: Update, context: CallbackContext) -> None:
    user_data['price'] = update.message.text
    bill = f"فاتورة بيع:\nالاسم: {user_data['name']}\nالمنتجات: {user_data['products']}\nالسعر: {user_data['price']}"
    update.message.reply_text(bill)

# الدالة الرئيسية
def main():
    # إضافة التوكن الخاص بك هنا
    updater = Updater("7229881570:AAHeGfWQFr0LibYjoPhwPyPXrlNpJhspe8M", use_context=True)

    dp = updater.dispatcher

    # ربط الأوامر بالدوال
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_name))

    # استقبال الرسائل النصية المتتابعة
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_products))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_price))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()