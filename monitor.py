import os
import asyncio
import io
import logging
import httpx
from aiohttp import web
from telethon import TelegramClient, events
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument

logging.basicConfig(level=logging.INFO)

API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']
MY_CHAT_ID = int(os.environ['MY_CHAT_ID'])
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')

CHANNELS = [
    'roganskayarespublika', 'ha_golovne', 'Vidklyuchenya_KHARKIV',
    'kharkiv_pishet', 'avariukaxarkiv', 'cxidua', 'alekseevka_kharkiv',
    'huyovy_kharkiv', 'sutnist_kh', 'cto_kharkov', 'carhub_kharkov',
    'kharkivlife', 'kharkov_media', 'suspilne_kharkiv', 'tipichnoe_xtz',
    'truexakharkiv', 'KharkivPolitics', 'kharkov_now', 'kholodnaiagora',
    'dumka_media', 'charkov_tut', 'kharkov_times', 'Kharkovski_region',
    'kharkivrl', 'otn_kharkov', 'povestkadnyakharkov', 'synegubov',
    'kharkivts', 'kharkiv_news_24', 'majestic_kh', 'kharkiv_misto_geroi',
    'napovestkeKh', 'jenya_zub_live_news', 'gwaramedia', 'nakipelovo',
    'place_kharkiv', 'hs_kharkiv', 'kharkiv_1654', 'qwuitetest',
    'monitor1654', 'bayrep_kh',
]

KEYWORDS = [
    # Мікрорайони
    'одеська',
    'одесская',
    'одеський',
    'основа',
    'основянський',
    'основянский',
    'нові дома',
    'новые дома',
    'немишлянський',
    'немишлянский',
    'немишляни',
    'немышляны',
    'жихар',
    'жихарь',
    'левада',
    'москалівка',
    'москалевка',
    'новожаново',
    'слобідський район',
    'слободской район',
    'верещаківка',
    'верещаковка',
    'артема',
    'павленки',
    'горбані',
    'горбани',
    'федорці',
    'федорцы',
    'чунихи',
    'дудківка',
    'дудковка',
    'заїківка',
    'заиковка',
    'балашівка',
    'балашовка',

    # Левада / Гагаріна
    'гагаріна',
    'гагарина',
    'район гагаріна',
    'район гагарина',

    # Навколишні міста та села
    'безлюдівка',
    'безлюдовка',
    'васищеве',
    'васищево',
    'мерефа',
    'високе',
    'высокое',
    'бабаї',
    'бабаи',
    'хорошеве',
    'хорошево',
    'хроли',
    'лелюки',
    'логачівка',
    'логачевка',
    'молчани',
    'молчаны',
    'котляри',
    'котляры',

    # Аеропорт
    'аеропорт основа',
    'аэропорт основа',


    # Вулиці Слобідського району
    'зернова вулиця',
    'зерновая улица',
    'вулиця зернова',
    'улица зерновая',
    'аеропортна вулиця',
    'улица аэропортная',
    'автодорожна вулиця',
    'улица автодорожная',
    'байрона проспект',
    'проспект байрона',
    'бельбецька вулиця',
    'вулиця гордона',
    'улица гордона',
    'дніпровська вулиця',
    'днепровская улица',
    'жасминовий бульвар',
    'жасминовый бульвар',
    'заозерна вулиця',
    'заозерная улица',
    'каштанова вулиця',
    'каштановая улица',
    'киргизька вулиця',
    'киргизская улица',
    'костичева вулиця',
    'улица костычева',
    'котляревського вулиця',
    'улица котляревского',
    'леонтовича вулиця',
    'улица леонтовича',
    'льва ландау проспект',
    'малишева вулиця',
    'улица малышева',
    'маршала федоренко вулиця',
    'улица маршала федоренко',
    'машинобудівна вулиця',
    'улица машиностроительная',
    'миру вулиця',
    'улица мира',
    'міцкевича вулиця',
    'улица мицкевича',
    'молодої гвардії вулиця',
    'улица молодой гвардии',
    'морозова вулиця',
    'улица морозова',
    'мухачова вулиця',
    'улица мухачева',
    'нестерова вулиця',
    'улица нестерова',
    'ньютона вулиця',
    'улица ньютона',
    'оренбурзька вулиця',
    'оренбургская улица',
    'переїзна вулиця',
    'улица переездная',
    'петра григоренка проспект',
    'проспект григоренка',
    'польова вулиця',
    'улица полевая',
    'пшенична вулиця',
    'улица пшеничная',
    'садовопаркова вулиця',
    'самаркандська вулиця',
    'самаркандская улица',
    'танкопія вулиця',
    'улица танкопия',
    'енергетична вулиця',
    'улица энергетическая',
    'вузлова вулиця',
    'балашовська вулиця',
    'дегтярьова вулиця',
    'улица дегтярева',
    'дизельна вулиця',
    'улица дизельная',
    'аерокосмічний проспект',
    'аэрокосмический проспект',
    'каденюка вулиця',
    'улица каденюка',
    'немишлянська вулиця',
    'немышлянская улица',
    'безлюдівська вулиця',
    'улица безлюдовская',
    'павла тичини вулиця',
    'улица павла тычины',
    'харківських дивізій вулиця',
    'улица харьковских дивизий',

    # Ринки та торгові об'єкти
    'комунальний ринок',
    'коммунальный рынок',
    'кінний ринок',
    'конный рынок',
    'автоград',

    # Метро
    'метро турбоатом',
    'метро заводська',
    'метро спортивна',
    'метро палац спорту',
    'метро масельського',

    # Проспекти та вулиці
    'проспект льва ландау',
    'просп льва ландау',
    'пр льва ландау',
    'проспект байрона',
    'просп байрона',
    'пр байрона',
    'аерокосмічний проспект',
    'аерокосмический проспект',
    'проспект петра григоренка',
    'вулиця каденюка',
    'улица каденюка',
    'вулиця ньютона',
    'улица ньютона',
    'вулиця малишева',
    'улица малышева',
    'вулиця павла тичини',
    'улица павла тычины',
    'вулиця немишлянська',
    'улица немышлянская',
    'вулиця безлюдівська',
    'улица безлюдовская',
    'вулиця енергетична',
    'улица энергетическая',
    'вулиця танкопія',
    'улица танкопия',
    'вулиця польова',
    'улица полевая',
    'вулиця машинобудівна',
    'улица машиностроительная',
    'вулиця аеропортна',
    'улица аэропортная',
    'вулиця малишева',
    'жасминовий бульвар',

    # Об\'єкти
    'завод малишева',
    'завод малышева',
    'турбоатом',
    'палац спорту',
    'дворец спорта',
    'рост одеський',
    'рост одесский',
    'sun mall',
    'сан молл',
    '17 лікарня',
    '17 больница',
    '18 лікарня',
    '18 больница',
    'хнувс',
    'металіст стадіон',
    'стадион металист',
]

AI_PROMPT = """Ти — фільтр новин для районного каналу Харкова.

Визнач чи стосується цей пост КОНКРЕТНО одного з цих місць:
- Вулиця Одеська та прилеглі вулиці
- Слобідський район Харкова
- Основянський район Харкова
- Нові Доми (район Харкова)
- Аеропорт Основа та прилеглий район
- Комунальний ринок на Одеській
- Проспект Байрона
- Проспект Аерокосмічний / Гагаріна
- Левада, Жихор
- Горбані, Павленки, Федорці

ПРАВИЛА:
- Загальні новини Харкова БЕЗ конкретного району = НІ
- Тривога/дрони/ракети БЕЗ конкретної вулиці = НІ
- Зеленський, НАТО, інші міста = НІ
- Відключення БЕЗ конкретного района = НІ
- Конкретна вулиця або місце з мого списку = ТАК

Відповідай ТІЛЬКИ: ТАК або НІ"""

async def check_with_gemini(text):
    if not GEMINI_API_KEY:
        return True
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [{"parts": [{"text": f"{AI_PROMPT}\n\nПост:\n{text[:500]}"}]}],
            "generationConfig": {"maxOutputTokens": 10, "temperature": 0}
        }
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(url, json=payload)
            data = response.json()
            answer = data["candidates"][0]["content"]["parts"][0]["text"].strip().upper()
            logging.info(f"Gemini: {answer}")
            return "ТАК" in answer or "TAK" in answer or "YES" in answer
    except Exception as e:
        logging.error(f"Помилка Gemini: {e}")
        return True

user_client = TelegramClient(
    'bot_session', API_ID, API_HASH,
    connection_retries=10,
    retry_delay=5,
    auto_reconnect=True,
)
bot_client = TelegramClient('bot', API_ID, API_HASH)

# Черга повідомлень — жоден пост не загубиться
message_queue = asyncio.Queue()

async def send_to_me(event, keyword, channel_name, channel_username):
    text = event.message.text or event.message.caption or ''
    first_line = text.strip().split('\n')[0][:100] if text.strip() else '...'
    caption = (
        f"🔴 {first_line}\n"
        f"{'─' * 30}\n"
        f"📍 Слово: «{keyword}»\n"
        f"Канал: @{channel_username}\n"
        f"{'─' * 30}\n"
        f"{text[:900]}"
    )

    if event.message.media:
        try:
            media = event.message.media
            if isinstance(media, MessageMediaPhoto):
                ext = '.jpg'
            elif isinstance(media, MessageMediaDocument):
                mime = media.document.mime_type or ''
                # Пропускаємо великі відео (більше 20МБ)
                if hasattr(media, 'document') and media.document.size > 20 * 1024 * 1024:
                    await bot_client.send_message(MY_CHAT_ID, caption + "\n\n📎 Відео занадто велике — дивись в оригіналі")
                    return
                if 'video' in mime:
                    ext = '.mp4'
                elif 'gif' in mime:
                    ext = '.gif'
                else:
                    ext = '.jpg'
            else:
                ext = '.jpg'

            buf = io.BytesIO()
            await user_client.download_media(event.message, buf)
            buf.seek(0)
            buf.name = f'media{ext}'
            await bot_client.send_file(MY_CHAT_ID, file=buf, caption=caption)
            return
        except Exception as e:
            logging.error(f"Помилка медіа: {e}")

    await bot_client.send_message(MY_CHAT_ID, caption)

# Обробник черги — обробляє пости по одному
async def queue_worker():
    logging.info("Черга запущена")
    while True:
        try:
            event, keyword = await message_queue.get()
            try:
                text = event.message.text or event.message.caption or ''

                logging.info(f"Знайдено: {keyword}. Перевіряю через Gemini...")
                is_relevant = await check_with_gemini(text)

                if not is_relevant:
                    logging.info(f"Gemini відхилив — не про наш район")
                    continue

                channel = await event.get_chat()
                channel_name = getattr(channel, 'title', 'Невідомий канал')
                channel_username = getattr(channel, 'username', '')

                logging.info(f"✅ Надсилаю з {channel_name}")
                await send_to_me(event, keyword, channel_name, channel_username)

            except Exception as e:
                logging.error(f"Помилка обробки посту: {e}")
            finally:
                message_queue.task_done()

        except Exception as e:
            logging.error(f"Помилка черги: {e}")
            await asyncio.sleep(1)

@user_client.on(events.NewMessage(chats=CHANNELS))
async def handler(event):
    try:
        text = event.message.text or event.message.caption or ''
        text_lower = text.lower()

        if not text_lower.strip():
            return

        for keyword in KEYWORDS:
            if keyword.lower() in text_lower:
                # Додаємо в чергу — не блокуємо основний потік
                await message_queue.put((event, keyword))
                logging.info(f"В черзі: {message_queue.qsize()} постів")
                break

    except Exception as e:
        logging.error(f"Помилка хендлера: {e}")

async def health_check(request):
    return web.Response(text="OK", status=200)

async def start_health_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    app.router.add_get('/health', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    logging.info(f"Health check сервер запущено на порту {port}")

async def main():
    await user_client.start()
    await bot_client.start(bot_token=BOT_TOKEN)

    print("✅ Бот запущен з Gemini AI фільтром!")
    print(f"📋 Слежу за {len(CHANNELS)} каналами")
    print(f"🔍 Мониторю {len(KEYWORDS)} ключевых слов")
    print("🤖 Gemini фільтр активний!")
    print("📬 Черга повідомлень активна!")
    print("👀 Слежу за каналами...")

    # Запускаємо health check сервер для UptimeRobot
    await start_health_server()

    # Запускаємо обробник черги паралельно
    asyncio.create_task(queue_worker())

    while True:
        try:
            await user_client.run_until_disconnected()
        except Exception as e:
            logging.error(f"З'єднання перервано: {e}. Перепідключаємось...")
            await asyncio.sleep(5)

asyncio.run(main())
