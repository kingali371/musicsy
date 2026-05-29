# استخدام Python 3.10 كقاعدة
FROM python:3.10-slim-buster

# تعيين مجلد العمل
WORKDIR /app

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y \
    ffmpeg \
    nodejs \
    npm \
    git \
    curl \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات
COPY requirements.txt .

# تثبيت مكتبات Python
RUN pip3 install --no-cache-dir -r requirements.txt

# نسخ جميع ملفات المشروع
COPY . .

# تعيين المنفذ لـ Render
ENV PORT=10000

# فتح المنفذ
EXPOSE $PORT

# أمر تشغيل البوت
CMD ["python3", "main.py"]
