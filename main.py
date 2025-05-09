import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '7224975779:AAEhPOso_u-qHooI7adz08ZgnSmU_nH02NY'
OWNER_ID = 5372240626  # ضع هنا معرفك الشخصي (ID)

bot = telebot.TeleBot(API_TOKEN)

# قائمة الأدمنز
admin_ids = {OWNER_ID}

# لوحة المفاتيح الخاصة بالمالك فقط
owner_markup = ReplyKeyboardMarkup(resize_keyboard=True)
owner_markup.add(
    KeyboardButton('➕ إضافة أدمن جديد'),
    KeyboardButton('📋 عرض قائمة الأدمنز')
)

# كلمات يتم تتبعها
KEYWORDS = ['ابي', 'يحل', 'يسوي', 'يقدر', 'أبي','يلخص','يشرح','ابغى','أبغى','أبغ','ابغ']

# عند بدء البوت
@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    if user_id == OWNER_ID:
        bot.send_message(user_id, "أهلاً بك، يمكنك إدارة الأدمنز عبر الأزرار التالية:", reply_markup=owner_markup)
    else:
        bot.send_message(user_id, "مرحبًا! هذا البوت مخصص فقط للمراقبة ولا يمكن استخدامه من قبل المستخدمين العاديين.")

# التعامل مع الأزرار (للمالك فقط)
@bot.message_handler(func=lambda m: m.text == '➕ إضافة أدمن جديد')
def ask_for_admin_id(message):
    if message.from_user.id == OWNER_ID:
        msg = bot.send_message(OWNER_ID, "أرسل الآن معرف (ID) الأدمن الجديد الذي تريد إضافته:")
        bot.register_next_step_handler(msg, add_admin_by_id)
    else:
        bot.send_message(message.chat.id, "هذا الخيار متاح للمالك فقط.")

def add_admin_by_id(message):
    try:
        new_admin_id = int(message.text.strip())
        if new_admin_id not in admin_ids:
            admin_ids.add(new_admin_id)
            bot.send_message(OWNER_ID, f"تمت إضافة الأدمن الجديد بنجاح: {new_admin_id}")
        else:
            bot.send_message(OWNER_ID, "هذا الأدمن مضاف بالفعل.")
    except ValueError:
        bot.send_message(OWNER_ID, "يرجى إرسال رقم معرف صحيح.")

# عرض قائمة الأدمنز
@bot.message_handler(func=lambda m: m.text == '📋 عرض قائمة الأدمنز')
def list_admins(message):
    if message.from_user.id == OWNER_ID:
        if not admin_ids:
            bot.send_message(OWNER_ID, "لا توجد أدمنز مضافين حالياً.")
        else:
            ids_list = "\n".join([str(aid) for aid in admin_ids])
            bot.send_message(OWNER_ID, f"قائمة الأدمنز الحاليين:\n{ids_list}")
    else:
        bot.send_message(message.chat.id, "هذا الخيار متاح للمالك فقط.")

# مراقبة الكلمات في الجروبات
@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_group_message(message):
    if message.chat.type in ['group', 'supergroup']:
        text = message.text.lower()
        for keyword in KEYWORDS:
            if keyword in text:
                user_info = f"المستخدم: {message.from_user.first_name} @{message.from_user.username or 'لا يوجد'}\nمعرّفه: {message.from_user.id}"
                full_message = f"تم رصد كلمة: \"{keyword}\"\n\nالرسالة:\n{text}\n\n{user_info}"
                for admin_id in admin_ids:
                    bot.send_message(admin_id, full_message)
                break

bot.infinity_polling()