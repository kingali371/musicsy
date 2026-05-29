import os
import sys
import logging
import asyncio
import threading
from flask import Flask, jsonify
from pyrogram import Client, idle
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatType
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

# إعداد Flask Web Server (لإبقاء البوت نشطاً على Render)
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return jsonify({
        "status": "active",
        "service": "CR Music Bot",
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
    """تشغيل خادم الويب"""
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

# التحقق من المتغيرات الأساسية
required_vars = ["API_ID", "API_HASH", "BOT_TOKEN", "STRING_SESSION"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    logger.error(f"❌ المتغيرات التالية مفقودة: {', '.join(missing_vars)}")
    sys.exit(1)

# الاتصال بقاعدة البيانات
try:
    mongo_uri = os.getenv("MONGO_DB_URI")
    if mongo_uri:
        mongo_client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        mongo_client.admin.command('ping')
        db = mongo_client.get_database("musicsy")
        logger.info("✅ تم الاتصال بـ MongoDB بنجاح")
    else:
        logger.warning("⚠️ MONGO_DB_URI غير موجود، سيتم العمل بدون قاعدة بيانات")
        db = None
except ServerSelectionTimeoutError:
    logger.error("❌ فشل الاتصال بـ MongoDB")
    db = None

# إعداد البوت
bot = Client(
    "MusicBot",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    in_memory=True
)

# أوامر البوت الأساسية
@bot.on_message()
async def echo(client: Client, message: Message):
    """الرد على الأوامر الأساسية"""
    if message.text and message.text.startswith("/start"):
        await message.reply_text(
            f"🎵 **{os.getenv('MUSIC_BOT_NAME', 'CR Music Bot')}**\n\n"
            "✅ البوت يعمل بشكل طبيعي!\n"
            "🎶 أرسل رابط يوتيوب لتشغيل الموسيقى\n"
            "📝 استخدم /help للمساعدة",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Channel", url="https://t.me/yourchannel")],
                [InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/youraccount")]
            ])
        )
    
    elif message.text and message.text.startswith("/ping"):
        start_time = message.date
        await message.reply_text("🏓 Pong!")
    
    elif message.text and message.text.startswith("/help"):
        help_text = """
🎵 **أوامر البوت**

**لتشغيل الموسيقى:**
- ارسل رابط يوتيوب مباشرة
- /play <اسم الأغنية> - تشغيل أغنية

**التحكم:**
- /pause - إيقاف مؤقت
- /resume - استئناف التشغيل
- /skip - تخطي الأغنية
- /stop - إيقاف التشغيل

**المعلومات:**
- /help - عرض هذه الرسالة
- /ping - اختبار سرعة البوت
        """
        await message.reply_text(help_text)

async def main():
    """تشغيل البوت"""
    try:
        # بدء تشغيل Web Server في خيط منفصل
        threading.Thread(target=run_web_server, daemon=True).start()
        logger.info("✅ تم تشغيل Web Server على المنفذ 10000")
        
        # بدء تشغيل البوت
        await bot.start()
        bot_info = await bot.get_me()
        logger.info(f"✅ تم تشغيل البوت بنجاح: {bot_info.first_name}")
        logger.info(f"📱 Username: @{bot_info.username}")
        logger.info(f"🆔 Bot ID: {bot_info.id}")
        
        # إرسال إشعار التشغيل إلى مجموعة اللوج
        log_group = os.getenv("LOG_GROUP_ID")
        if log_group and db:
            try:
                await bot.send_message(
                    int(log_group),
                    f"✅ **البوت يعمل الآن!**\n\n"
                    f"🎵 **الاسم:** {os.getenv('MUSIC_BOT_NAME')}\n"
                    f"🕐 **الوقت:** {asyncio.get_event_loop().time()}"
                )
            except:
                pass
        
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
