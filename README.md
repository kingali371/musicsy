# 🎵 CR Music Bot

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/kingali371/musicsy)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?repo=https://github.com/kingali371/musicsy)

A Powerful Telegram Music Player Bot written in Python with Pyrogram and Py-Tgcalls.

---

## 🚀 Features

- 🎵 High quality music streaming
- 📝 Queue management system
- 🔍 Search songs on YouTube
- 📢 Voice chat support
- 🎚️ Interactive control buttons
- ⚡ Fast and reliable
- 💾 MongoDB database support
- 🔄 Auto reconnect

---

## 📋 Requirements

- Python 3.10+
- MongoDB Database
- Telegram API ID & Hash
- Bot Token from @BotFather

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_ID` | Get from [my.telegram.org](https://my.telegram.org) | ✅ |
| `API_HASH` | Get from [my.telegram.org](https://my.telegram.org) | ✅ |
| `BOT_TOKEN` | Get from [@BotFather](https://t.me/BotFather) | ✅ |
| `STRING_SESSION` | Pyrogram string session | ✅ |
| `OWNER_ID` | Your Telegram user ID | ✅ |
| `LOG_GROUP_ID` | Group ID for logs | ✅ |
| `MONGO_DB_URI` | MongoDB connection URI | ❌ |
| `MUSIC_BOT_NAME` | Name of your bot | ❌ |

---

## 🚀 Deployment

### Deploy to Render (Recommended)

1. Click the **Deploy to Render** button above
2. Connect your GitHub repository
3. Add all required environment variables
4. Click **Deploy**

### Deploy Locally

```bash
# Clone the repository
git clone https://github.com/kingali371/musicsy.git
cd musicsy

# Install dependencies
pip install -r requirements.txt

# Create .env file with your variables
cp .env.example .env
# Edit .env with your values

# Run the bot
python3 main.py




## 📋 المتغيرات المطلوبة (Required)

| Variable | Description | Required |
|----------|-------------|----------|
| `API_ID` | Get from [my.telegram.org](https://my.telegram.org) | ✅ **مطلوب** |
| `API_HASH` | Get from [my.telegram.org](https://my.telegram.org) | ✅ **مطلوب** |
| `BOT_TOKEN` | Get from [@BotFather](https://t.me/BotFather) | ✅ **مطلوب** |
| `STRING_SESSION` | Pyrogram string session | ✅ **مطلوب** |
| `OWNER_ID` | Your Telegram user ID | ✅ **مطلوب** |
| `LOG_GROUP_ID` | Group ID for logs | ✅ **مطلوب** |

## 📝 المتغيرات الاختيارية (Optional)

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `MONGO_DB_URI` | MongoDB connection URI | `None` (بدون قاعدة بيانات) |
| `MUSIC_BOT_NAME` | Name of your bot | `CR Music Bot` |
| `PORT` | Web server port | `10000` |

> **ملاحظة:** المتغيرات الاختيارية يمكن تركها فارغة، وسيعمل البوت بشكل طبيعي.
