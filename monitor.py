from telethon import TelegramClient, events
import asyncio

# ===== ТВОИ ДАННЫЕ (вставь новые после сброса) =====
API_ID = '39670597'
API_HASH = 'cdef744651ea328b57a992c646e38d28'
BOT_TOKEN = '8577340382:AAEDvKbJQktw7pAbNwUBM38q-Znl7HdV8BU'
MY_CHAT_ID = '6357875962'  # узнаешь ниже

# ===== КАНАЛЫ КОНКУРЕНТОВ =====
CHANNELS = [
    'kharkivlife',
    'huyovy_kharkiv',
    'truexakharkiv',
]

# ===== КЛЮЧЕВЫЕ СЛОВА ТВОЕГО РАЙОНА =====
KEYWORDS = [
    'одесская',
    'одеська',
    'основа',
    'слобідський район',
    'слободской район',
    'левада',
    'коммунальный рынок',
    'комунальний ринок',
]

# ===== КОД (не трогай) =====
client = TelegramClient('monitor_session', API_ID, API_HASH)
bot = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.NewMessage(chats=CHANNELS))
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

            await bot.send_message(int(MY_CHAT_ID), msg)
            break  # чтобы не дублировать если несколько ключевых слов

async def main():
    await client.start()
    print("✅ Мониторинг запущен! Слежу за каналами...")
    await client.run_until_disconnected()

with bot:
    bot.loop.run_until_complete(main())
