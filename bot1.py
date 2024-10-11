import telebot
import mysql.connector
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# توكن البوت الخاص بك
TOKEN = '8094828325:AAHkJ9Ej-drEH5AZctO6JzGNAEkAoM6SAOs'
bot = telebot.TeleBot(TOKEN)

# الاتصال بقاعدة البيانات MySQL
db = mysql.connector.connect(
    host="localhost",
    user="your_mysql_user",
    password="your_mysql_password",
    database="your_database_name"
)
cursor = db.cursor()

# دالة لإنشاء المستخدم في قاعدة البيانات إذا لم يكن موجودًا
def create_user(user_id, username):
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO users (user_id, username, balance) VALUES (%s, %s, %s)", (user_id, username, 100))
        db.commit()

# دالة لعرض الرصيد
@bot.message_handler(commands=['balance'])
def check_balance(message):
    user_id = message.chat.id
    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    balance = cursor.fetchone()[0]
    bot.reply_to(message, f"رصيدك الحالي هو: {balance} دينار.")

# دالة لعرض المنتجات
@bot.message_handler(commands=['products'])
def show_products(message):
    cursor.execute("SELECT product_id, name, price FROM products")
    products = cursor.fetchall()
    if products:
        response = "المنتجات المتاحة:\n"
        for product in products:
            response += f"{product[0]}. {product[1]} - {product[2]} دينار\n"
        bot.reply_to(message, response)
    else:
        bot.reply_to(message, "لا توجد منتجات متاحة حالياً.")

# دالة لشراء المنتجات
@bot.message_handler(commands=['buy'])
def buy_product(message):
    try:
        product_id = int(message.text.split()[1])
        user_id = message.chat.id

        # التحقق من وجود المنتج
        cursor.execute("SELECT price FROM products WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        if not product:
            bot.reply_to(message, "المنتج غير موجود.")
            return

        price = product[0]

        # التحقق من رصيد المستخدم
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        balance = cursor.fetchone()[0]
        if balance < price:
            bot.reply_to(message, "رصيدك غير كافٍ لإتمام هذه العملية.")
        else:
            # تحديث رصيد المستخدم
            new_balance = balance - price
            cursor.execute("UPDATE users SET balance = %s WHERE user_id = %s", (new_balance, user_id))
            db.commit()
            bot.reply_to(message, "تم شراء المنتج بنجاح.")
    except IndexError:
        bot.reply_to(message, "يرجى تحديد معرف المنتج.")

# دالة لبدء التفاعل مع المستخدم
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    username = message.chat.username
    create_user(user_id, username)
    bot.reply_to(message, "مرحباً بك في متجرنا! استخدم /products لعرض المنتجات و /buy [معرف المنتج] لشراء منتج.")

# تشغيل البوت
bot.polling()
