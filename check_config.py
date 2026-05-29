#!/usr/bin/env python3
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# قائمة المتغيرات المطلوبة فقط
required_vars = [
    "API_ID",
    "API_HASH", 
    "BOT_TOKEN",
    "STRING_SESSION",
    "OWNER_ID",
    "LOG_GROUP_ID"
]

# المتغيرات الاختيارية
optional_vars = [
    "MONGO_DB_URI",
    "MUSIC_BOT_NAME",
    "PORT"
]

print("🔍 التحقق من متغيرات البيئة...\n")
print("="*50)
print("📋 المتغيرات المطلوبة:")
print("="*50)

missing = []
for var in required_vars:
    value = os.getenv(var)
    if value:
        # إخفاء القيم الحساسة
        if var in ["API_HASH", "BOT_TOKEN", "STRING_SESSION"]:
            print(f"✅ {var} = {value[:10]}... (مخفي)")
        else:
            print(f"✅ {var} = {value}")
    else:
        print(f"❌ {var} = غير موجود")
        missing.append(var)

print("\n" + "="*50)
print("📝 المتغيرات الاختيارية:")
print("="*50)

for var in optional_vars:
    value = os.getenv(var)
    if value:
        print(f"ℹ️ {var} = {value}")
    else:
        print(f"⚠️ {var} = غير موجود (اختياري)")

print("\n" + "="*50)

if missing:
    print(f"\n❌ المتغيرات المفقودة: {', '.join(missing)}")
    print("📝 يرجى إضافة جميع المتغيرات المطلوبة في ملف .env")
    sys.exit(1)
else:
    print("\n✅ جميع المتغيرات المطلوبة موجودة!")
    print("🚀 يمكنك تشغيل البوت الآن")
    sys.exit(0)
