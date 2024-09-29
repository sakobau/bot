from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# تعيين التوكن الخاص بالبوت
TOKEN = '7889761662:AAETDbWkCIX_sDXEQWai9LYeMkdg7NAtUoE'

# وظيفة معالجة أمر /start
def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    # قيمة رصيد الحساب (ستكون متغيرة حسب البيانات المخزنة)
    account_balance = 0  # يمكن تحديثها من قبل المطور

    # إعداد الكليشة والزر "رصيد حسابي"
    welcome_message = "مرحبا بك في متجر ســـــــــــوبر تــــــكنو للخدمات الالكترونية\nللاستفسار مراسلة المطور @m_55mg"
    button_1 = InlineKeyboardButton("تعبئة رصيد حسابي", callback_data='balance_fill')
    button_2 = InlineKeyboardButton("كارت هاتف", callback_data='phone_card')
    button_3 = InlineKeyboardButton("كارت شحن العاب", callback_data='game_card')
    button_4 = InlineKeyboardButton("كارت تطبيقات", callback_data='app_card')
    
    keyboard = [[button_1, button_2], [button_3, button_4]]
    markup = InlineKeyboardMarkup(keyboard)

    # إرسال الرسالة مع الأزرار
    update.message.reply_text(welcome_message, reply_markup=markup)

    # إرسال زر "رصيد حسابي" في الأعلى
    update.message.reply_text(f"رصيد حسابي: {account_balance}", reply_markup=markup)

# معالجة الأزرار
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    if query.data == 'balance_fill':
        # هنا يتم إضافة منطق تعبئة الرصيد من قبل المطور
        query.edit_message_text(text="أنت الآن في صفحة تعبئة الرصيد.")
    elif query.data == 'phone_card':
        query.edit_message_text(text="لقد اخترت كارت الهاتف.")
    elif query.data == 'game_card':
        query.edit_message_text(text="لقد اخترت كارت شحن الألعاب.")
    elif query.data == 'app_card':
        query.edit_message_text(text="لقد اخترت كارت التطبيقات.")

# الدالة الرئيسية لتشغيل البوت
def main():
    updater = Updater(TOKEN)

    # إضافة معالجي الأوامر
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
