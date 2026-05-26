import os
import asyncio
import io
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

# ===== ДАННЫЕ БЕРУТСЯ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ =====
API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']
MY_CHAT_ID = int(os.environ['MY_CHAT_ID'])

# ===== КАНАЛЫ КОНКУРЕНТОВ =====
CHANNELS = [
    'roganskayarespublika',
    'ha_golovne',
    'Vidklyuchenya_KHARKIV',
    'kharkiv_pishet',
    'avariukaxarkiv',
    'cxidua',
    'alekseevka_kharkiv',
    'huyovy_kharkiv',
    'sutnist_kh',
    'cto_kharkov',
    'carhub_kharkov',
    'kharkivlife',
    'kharkov_media',
    'suspilne_kharkiv',
    'tipichnoe_xtz',
    'truexakharkiv',
    'KharkivPolitics',
    'kharkov_now',
    'kholodnaiagora',
    'dumka_media',
    'charkov_tut',
    'kharkov_times',
    'Kharkovski_region',
    'kharkivrl',
    'otn_kharkov',
    'povestkadnyakharkov',
    'synegubov',
    'kharkivts',
    'kharkiv_news_24',
    'majestic_kh',
    'kharkiv_misto_geroi',
    'napovestkeKh',
    'jenya_zub_live_news',
    'gwaramedia',
    'nakipelovo',
    'place_kharkiv',
    'hs_kharkiv',
    'kharkiv_1654',
    'qwuitetest',
]

# ===== КЛЮЧЕВЫЕ СЛОВА =====
KEYWORDS = [
    'одесская', 'одеська', 'ул одесская', 'вул одеська',
    'байрона', 'проспект байрона', 'пр байрона',
    'аэрокосмический', 'аерокосмічний',
    'гагарина', 'гагаріна', 'проспект гагарина',
    'качановская', 'качанівська',
    'грозненская', 'грозненська',
    'южнопроектная', 'південнопроектна',
    'зерновая', 'зернова',
    'павла тычины', 'павла тичини',
    'вокзальная', 'вокзальна',
    'гольдбергівська', 'каденюка', 'ньютона',
    'льва ландау', 'проспект льва ландау',
    'героев сталинграда', 'героїв сталінграда',
    'трасса м18', 'траса м18', 'м18',
    'основа', 'основянский', 'основянський',
    'слободской', 'слобідський',
    'холодногорский', 'холодногірський',
    'немышлянский', 'немишлянський',
    'левада', 'новые дома', 'нові доми',
    'верещаковка', 'верещаківка',
    'заиковка', 'москалевка', 'москалівка',
    'красный луч', 'горбани', 'павленки',
    'федорцы', 'чунихи', 'дудковка',
    'коммунальный рынок', 'комунальний ринок',
    'аэропорт', 'аеропорт',
    'жк одесский', 'жк одеський', 'жк основа',
    'новостройки основа', 'новобудови основа',
    'квартиры основа', 'квартири основа',
    'атб основа', 'сільпо основа',
    'нова пошта основа', 'нова пошта одеська',
    'маршрутка одесская', 'тролейбус одеська',
    'відключення світла основа', 'отключение света основа',
    'відключення води основа', 'отключение воды основа',
    'відключення газу основа',
    'обстріл основа', 'прильот основа',
    'пожежа основа', 'дтп одесская', 'дтп основа',
    'завод малышева', 'турбоатом',
]

# ===== КОД =====
user_client = TelegramClient('bot_session', API_ID, API_HASH)
bot_client = TelegramClient('bot', API_ID, API_HASH)

async def main():
    await user_client.start()
    await bot_client.start(bot_token=BOT_TOKEN)
    print("✅ Бот запущен!")
    print(f"📋 Слежу за {len(CHANNELS)} каналами")
    print(f"🔍 Мониторю {len(KEYWORDS)} ключевых слов")

    @user_client.on(events.NewMessage(chats=CHANNELS))
    async def handler(event):
        text = event.message.text or event.message.caption or ''
        text_lower = text.lower()

        for keyword in KEYWORDS:
            if keyword.lower() in text_lower:
                channel = await event.get_chat()
                channel_name = getattr(channel, 'title', 'Неизвестный канал')
                channel_username = getattr(channel, 'username', '')

                header = (
                    f"📢 Новый пост из канала: {channel_name}\n"
                    f"🔗 @{channel_username}\n"
                    f"🔍 Найдено по слову: «{keyword}»\n"
                    f"{'─' * 30}\n"
                )

                caption = header + text[:900]

                if event.message.media:
                    try:
                        media = event.message.media

                        # Определяем расширение файла
                        if isinstance(media, MessageMediaPhoto):
                            ext = '.jpg'
                        elif isinstance(media, MessageMediaDocument):
                            mime = media.document.mime_type or ''
                            if 'video' in mime:
                                ext = '.mp4'
                            elif 'gif' in mime:
                                ext = '.gif'
                            elif 'image' in mime:
                                ext = '.jpg'
                            else:
                                ext = '.jpg'
                        else:
                            ext = '.jpg'

                        # Скачиваем в память
                        buf = io.BytesIO()
                        await user_client.download_media(event.message, buf)
                        buf.seek(0)
                        buf.name = f'media{ext}'

                        await bot_client.send_file(
                            MY_CHAT_ID,
                            file=buf,
                            caption=caption
                        )
                    except Exception as e:
                        print(f"Ошибка медиа: {e}")
                        await bot_client.send_message(MY_CHAT_ID, caption)
                else:
                    await bot_client.send_message(MY_CHAT_ID, caption)
                break

    print("👀 Слежу за каналами...")
    await user_client.run_until_disconnected()

asyncio.run(main())
