#!/bin/bash

# تحديث الحزم وتثبيت ffmpeg و nodejs
apt-get update
apt-get install -y ffmpeg nodejs npm

# تثبيت المتطلبات Python
pip install --upgrade pip
pip install -r requirements.txt

# تشغيل البوت
python3 main.py
