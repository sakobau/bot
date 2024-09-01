from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

def start(update: Update, context: CallbackContext):
    update.message.reply_text('مرحباً بك!')

def main():
    updater = Updater("7159716290:AAGTxMlWTfNZ9nI6dz0DbDanqP3TMw8u6SM")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()