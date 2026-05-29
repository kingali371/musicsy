import os
import sys
import logging
import asyncio
import threading
from flask import Flask
from pyrogram import Client, idle
from dotenv import load_dotenv

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
    return "Bot is running!", 200

@web_app.route('/health')
def health():
    return {"status": "alive", "service": "Telegram Music Bot"}, 200

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port, debug=False)

# التحقق من المتغيرات الأساسية
required_vars = ["API_ID", "API_HASH", "BOT_TOKEN", "STRING_SESSION"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    logger.error(f"❌ المتغيرات التالية مفقودة: {', '.join(missing_vars)}")
    sys.exit(1)

async def main():
    """تشغيل البوت"""
    try:
        # بدء تشغيل Web Server في خيط منفصل
        threading.Thread(target=run_web_server, daemon=True).start()
        
        # إعداد البوت
        bot = Client(
            "MusicBot",
            api_id=int(os.getenv("API_ID")),
            api_hash=os.getenv("API_HASH"),
            bot_token=os.getenv("BOT_TOKEN"),
            in_memory=True
        )
        
        await bot.start()
        logger.info(f"✅ تم تشغيل البوت بنجاح: {bot.me.first_name}")
        
        # إبقاء البوت يعمل
        await idle()
        
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}")
        sys.exit(1)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
