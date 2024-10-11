import telebot
import mysql.connector

# توكن البوت
TOKEN = "8094828325:AAHkJ9Ej-drEH5AZctO6JzGNAEkAoM6SAOs"
bot = telebot.TeleBot(TOKEN)

# إعداد الاتصال بقاعدة بيانات MySQL
db_config = {
    'user': 'اسم_المستخدم',         # اسم المستخدم لقاعدة البيانات
    'password': 'كلمة_المرور',       # كلمة مرور قاعدة البيانات
    'host': 'اسم_المضيف',           # عادةً 'localhost' في PythonAnywhere
    'database': 'اسم_قاعدة_البيانات'  # اسم قاعدة البيانات الخاصة بك
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# إنشاء الجداول إذا لم تكن موجودة
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id BIGINT PRIMARY KEY,
                    username VARCHAR(255),
                    balance FLOAT,
                    card_number VARCHAR(255))''')

cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    product_id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    price FLOAT,
                    stock INT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id BIGINT,
                    product_id INT,
                    amount FLOAT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (product_id) REFERENCES products(product_id))''')

conn.commit()

# إضافة بعض المنتجات بشكل افتراضي
def add_default_products():
    cursor.execute("INSERT INTO products (name, price, stock) VALUES ('منتج 1', 100, 10)")
    cursor.execute("INSERT INTO products (name, price, stock) VALUES ('منتج 2', 200, 5)")
    cursor.execute("INSERT INTO products (name, price, stock) VALUES ('منتج 3', 300, 2)")
    conn.commit()

add_default_products()

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    
    if user is None:
        card_number = f"CARD{user_id}"
        cursor.execute("INSERT INTO users (user_id, username, balance, card_number) VALUES (%s, %s, %s, %s)",
                       (user_id, message.chat.username, 0, card_number))
        conn.commit()
        bot.reply_to(message, f"مرحبا {message.chat.username}! تم إنشاء حسابك بنجاح.")
    else:
        bot.reply_to(message, "لديك حساب بالفعل!")

@bot.message_handler(commands=['balance'])
def check_balance(message):
    user_id = message.chat.id
    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    
    if user:
        balance = user[0]
        bot.reply_to(message, f"رصيدك الحالي هو: {balance} دينار.")
    else:
        bot.reply_to(message, "يجب عليك التسجيل أولاً باستخدام /start.")

@bot.message_handler(commands=['products'])
def show_products(message):
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    product_list = ""
    for product in products:
        product_list += f"{product[1]} - {product[2]} دينار - المتوفر: {product[3]}\n"
    bot.reply_to(message, product_list if product_list else "لا توجد منتجات متاحة.")

@bot.message_handler(commands=['buy'])
def buy_product(message):
    user_id = message.chat.id
    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    
    if not user:
        bot.reply_to(message, "يجب عليك التسجيل أولاً باستخدام /start.")
        return

    user_balance = user[0]
    product_id = message.text.split()[1] if len(message.text.split()) > 1 else None

    if not product_id:
        bot.reply_to(message, "يرجى تحديد معرف المنتج الذي تريد شراءه.")
        return

    cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
    product = cursor.fetchone()
    
    if product is None:
        bot.reply_to(message, "هذا المنتج غير موجود.")
        return

    product_price = product[2]
    if user_balance >= product_price:
        # خصم المبلغ وتحديث الرصيد
        new_balance = user_balance - product_price
        cursor.execute("UPDATE users SET balance = %s WHERE user_id = %s", (new_balance, user_id))
        cursor.execute("INSERT INTO transactions (user_id, product_id, amount) VALUES (%s, %s, %s)",
                       (user_id, product_id, product_price))
        conn.commit()
        bot.reply_to(message, f"تم شراء {product[1]} بنجاح! رصيدك المتبقي هو: {new_balance} دينار.")
    else:
        bot.reply_to(message, "رصيدك غير كافٍ لشراء هذا المنتج.")

@bot.message_handler(commands=['recharge'])
def recharge_balance(message):
    user_id = message.chat.id
    amount = float(message.text.split()[1]) if len(message.text.split()) > 1 else None

    if amount is None:
        bot.reply_to(message, "يرجى إدخال المبلغ المراد إضافته.")
        return

    cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, user_id))
    conn.commit()
    bot.reply_to(message, f"تم إعادة شحن رصيدك بمبلغ {amount} دينار.")

# تشغيل البوت
bot.polling()

# أغلق الاتصال عند الانتهاء (يمكنك استخدام try/except لضمان الإغلاق في حالة الأخطاء)
conn.close()
