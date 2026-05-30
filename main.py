import os
import sys
import logging
import asyncio
import threading
from flask import Flask, jsonify
from pyrogram import Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# تحميل المتغيرات البيئية
load_dotenv()

# إعداد التسجيل
logging.basicConfig(
    format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# إعداد Flask Web Server
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    bot_name = os.getenv("MUSIC_BOT_NAME", "CR Music Bot")
    return jsonify({
        "status": "active",
        "service": bot_name,
        "message": "Bot is running successfully!"
    }), 200

@web_app.route('/health')
def health():
    return jsonify({
        "status": "alive",
        "service": "Telegram Music Bot",
        "version": "1.0.0"
    }), 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

# التحقق من المتغيرات الأساسية فقط (بدون MONGO_DB_URI و MUSIC_BOT_NAME)
required_vars = [
    "API_ID", 
    "API_HASH", 
    "BOT_TOKEN", 
    "STRING_SESSION", 
    "OWNER_ID", 
    "LOG_GROUP_ID"
]

missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    logger.error("❌ المتغيرات التالية مفقودة:")
    for var in missing_vars:
        logger.error(f"   - {var}")
    logger.info("\n📝 يرجى إضافة جميع المتغيرات المطلوبة قبل تشغيل البوت")
    sys.exit(1)

# الحصول على اسم البوت (اختياري)
BOT_NAME = os.getenv("MUSIC_BOT_NAME", "CR Music Bot")
logger.info(f"🎵 اسم البوت: {BOT_NAME}")

# الاتصال بقاعدة البيانات (اختياري)
db = None
mongo_client = None
mongo_uri = os.getenv("MONGO_DB_URI")

if mongo_uri:
    try:
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        mongo_client.admin.command('ping')
        db = mongo_client.get_database("musicsy")
        logger.info("✅ تم الاتصال بـ MongoDB بنجاح")
    except ServerSelectionTimeoutError:
        logger.warning("⚠️ فشل الاتصال بـ MongoDB - سيتم العمل بدون قاعدة بيانات")
        db = None
    except Exception as e:
        logger.warning(f"⚠️ خطأ في الاتصال بـ MongoDB: {e} - سيتم العمل بدون قاعدة بيانات")
        db = None
else:
    logger.info("ℹ️ MONGO_DB_URI غير موجود - سيتم العمل بدون قاعدة بيانات")

# إعداد البوت
bot = Client(
    "MusicBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    in_memory=True
)

@bot.on_message()
async def handle_messages(client: Client, message: Message):
    """الرد على الأوامر الأساسية"""
    if message.text and message.text.startswith("/start"):
        # عرض حالة قاعدة البيانات
        db_status = "✅ متصلة" if db else "⚠️ غير متصلة"
        
        await message.reply_text(
            f"🎵 **{BOT_NAME}**\n\n"
            f"✅ مرحباً {message.from_user.mention}!\n"
            f"🤖 البوت يعمل بشكل طبيعي!\n"
            f"💾 قاعدة البيانات: {db_status}\n\n"
            f"🎶 أرسل رابط يوتيوب لتشغيل الموسيقى\n"
            f"📝 استخدم /help للمساعدة",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Channel", url="https://t.me/def_Zoka")],
                [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/youraccount")]
            ])
        )
    
    elif message.text and message.text.startswith("/ping"):
        # التحقق من اتصال قاعدة البيانات إذا كانت موجودة
        if db:
            try:
                mongo_client.admin.command('ping')
                db_status = "✅ متصلة"
            except:
                db_status = "⚠️ غير متصلة"
        else:
            db_status = "ℹ️ غير مستخدمة"
        
        await message.reply_text(
            f"🏓 **{BOT_NAME}**\n"
            f"🕐 الوقت: {message.date}\n"
            f"💾 قاعدة البيانات: {db_status}"
        )
    
    elif message.text and message.text.startswith("/help"):
        help_text = f"""
🎵 **{BOT_NAME} - المساعدة**

**🎧 أوامر التشغيل:**
- ارسل رابط يوتيوب مباشرة
- `/play <اسم الأغنية>` - تشغيل أغنية

**🎮 أوامر التحكم:**
- `/pause` - إيقاف مؤقت
- `/resume` - استئناف التشغيل
- `/skip` - تخطي الأغنية
- `/stop` - إيقاف التشغيل

**ℹ️ أوامر عامة:**
- `/start` - بدء البوت
- `/help` - عرض المساعدة
- `/ping` - اختبار البوت

**👑 المطور:** @youraccount
        """
        await message.reply_text(help_text)

async def main():
    """تشغيل البوت"""
    try:
        # بدء تشغيل Web Server
        threading.Thread(target=run_web_server, daemon=True).start()
        logger.info(f"✅ تم تشغيل Web Server للمنفذ {os.environ.get('PORT', 10000)}")
        
        # بدء تشغيل البوت
        await bot.start()
        bot_info = await bot.get_me()
        logger.info(f"✅ تم تشغيل البوت بنجاح: {BOT_NAME}")
        logger.info(f"📱 Username: @{bot_info.username}")
        logger.info(f"🆔 Bot ID: {bot_info.id}")
        logger.info(f"🎵 Bot Name: {BOT_NAME}")
        
        if db:
            logger.info(f"💾 MongoDB: متصل ✅")
        else:
            logger.info(f"💾 MongoDB: غير مستخدم ⚠️")
        
        # إرسال إشعار التشغيل
        log_group = os.getenv("LOG_GROUP_ID")
        if log_group:
            try:
                db_status = "✅ متصلة" if db else "⚠️ غير متصلة (اختياري)"
                await bot.send_message(
                    int(log_group),
                    f"✅ **{BOT_NAME} يعمل الآن!**\n\n"
                    f"🎵 **الاسم:** {BOT_NAME}\n"
                    f"💾 **قاعدة البيانات:** {db_status}\n"
                    f"🕐 **التاريخ:** {asyncio.get_event_loop().time()}\n"
                    f"✅ **الحالة:** نشط"
                )
                logger.info("📨 تم إرسال إشعار التشغيل إلى مجموعة اللوج")
            except Exception as e:
                logger.warning(f"⚠️ لم يتم إرسال الإشعار: {e}")
        
        # إبقاء البوت يعمل
        await idle()
        
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}")
        sys.exit(1)
    finally:
        await bot.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {e}")
