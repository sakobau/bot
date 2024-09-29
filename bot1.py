from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# متغير لتخزين رصيد الحساب (يتم تحديثه فقط بواسطة المطور)
account_balance = 0

# اسم المستخدم الخاص بالمطور الذي يمكنه تعبئة الرصيد
developer_username = "m_55mg"  # استبدل بـ اسم المستخدم الخاص بالمطور

# تابع لتنفيذ الأمر /start عند الضغط عليه
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton(f"رصيد حسابي: {account_balance}", callback_data='balance')],
        [InlineKeyboardButton("تعبئة رصيد حسابي", callback_data='top_up')],
        [InlineKeyboardButton("كارت هاتف", callback_data='mobile_card')],
        [InlineKeyboardButton("كارت شحن العاب", callback_data='game_card')],
        [InlineKeyboardButton("كارت تطبيقات", callback_data='app_card')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'مرحبا بك في متجر ســـــــــــوبر تــــــكنو للخدمات الالكترونية\n'
        'للاستفسار مراسلة المطور @m_55mg',
        reply_markup=reply_markup
    )

# تابع لتحديث رصيد الحساب فقط بواسطة المطور
def top_up(update: Update, context: CallbackContext) -> None:
    if update.message.from_user.username == developer_username:
        try:
            new_balance = int(context.args[0])
            global account_balance
            account_balance = new_balance
            update.message.reply_text(f"تم تحديث رصيد الحساب إلى: {account_balance}")
        except (IndexError, ValueError):
            update.message.reply_text("يرجى إدخال رصيد صالح بعد الأمر.")
    else:
        update.message.reply_text("فقط المطور يمكنه تحديث رصيد الحساب.")

# تابع لمعالجة الضغط على الأزرار
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'top_up':
        query.edit_message_text(text="للتعبئة، استخدم الأمر التالي: /topup <المبلغ>")
    elif query.data == 'mobile_card':
        query.edit_message_text(text="تم اختيار كارت الهاتف.")
    elif query.data == 'game_card':
        query.edit_message_text(text="تم اختيار كارت شحن الألعاب.")
    elif query.data == 'app_card':
        query.edit_message_text(text="تم اختيار كارت التطبيقات.")
    elif query.data == 'balance':
        query.edit_message_text(text=f"رصيد حسابك الحالي هو: {account_balance}")

def main():
    # أدخل مفتاح API الخاص بالبوت هنا
    updater = Updater("8131016207:AAHC6QQIHw48c-XHCRQAYMOKk5PUu3n3vws", use_context=True)

    # إضافة معالج الأمر /start
    updater.dispatcher.add_handler(CommandHandler("start", start))

    # إضافة معالج الأوامر لتعبئة الرصيد
    updater.dispatcher.add_handler(CommandHandler("topup", top_up))

    # إضافة معالج الضغط على الأزرار
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
