import os
import asyncio
from telethon import TelegramClient, events

# ===== ДАННЫЕ БЕРУТСЯ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ =====
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']
MY_CHAT_ID = int(os.environ['MY_CHAT_ID'])

# ===== КАНАЛЫ КОНКУРЕНТОВ =====
CHANNELS = [
    'kharkivlife',
    'huyovy_kharkiv',
    'truexakharkiv',
]

# ===== КЛЮЧЕВЫЕ СЛОВА =====
KEYWORDS = [
    'одесская',
    'одеська',
    'основа',
    'слобідський район',
    'слободской район',
    'левада',
    'коммунальный рынок',
    'комунальний ринок',
    'аэропорт',
    'аеропорт',
]

# ===== КОД =====
bot = TelegramClient('bot_session', API_ID, API_HASH)

async def main():
    await bot.start(bot_token=BOT_TOKEN)
    print("✅ Бот запущен!")

    @bot.on(events.NewMessage(chats=CHANNELS))
    async def handler(event):
        text = event.message.text or ''
        text_lower = text.lower()

        for keyword in KEYWORDS:
            if keyword.lower() in text_lower:
                channel = await event.get_chat()
                channel_name = getattr(channel, 'title', 'Неизвестный канал')
                channel_username = getattr(channel, 'username', '')

                msg = (
                    f"📢 Новый пост из канала: {channel_name}\n"
                    f"🔗 @{channel_username}\n"
                    f"🔍 Найдено по слову: «{keyword}»\n"
                    f"{'─' * 30}\n"
                    f"{text[:1000]}"
                )

                await bot.send_message(MY_CHAT_ID, msg)
                break

    print("👀 Слежу за каналами...")
    await bot.run_until_disconnected()

asyncio.run(main())
