from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import requests
from pyrogram.types import Message

from bs4 import BeautifulSoup
from pyrogram.types import ChatPermissions
import subprocess
import time
from time import sleep
import random
import wikipediaapi #pip install Wikipedia-API
import random
import asyncio

from pyrogram import Client

from pyrogram import Client

app = Client(
    "my_account",
    api_id=10503380,
    api_hash="6cdc62f566b0320963e2673a3c8a8ff2"
)

# Команда type
@app.on_message(filters.command("type", prefixes=".") & filters.me)
def type(_, msg):
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = "" # to be printed
    typing_symbol = "▒"
    while(tbp != orig_text):
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.01) # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.01)

        except FloodWait as e:
            sleep(e.x)

R = "❤️"
W = "🤍"

heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]
joined_heart = "\n".join(heart_list)

heartlet_len = joined_heart.count(R)

SLEEP = 0.1


async def _wrap_edit(message: Message, text: str):
    """Floodwait-safe utility wrapper for edit"""
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.x)


async def phase1(message: Message):
    """Big scroll"""
    BIG_SCROLL = "🧡💛💚💙💜🖤🤎"
    await _wrap_edit(message, joined_heart)
    for heart in BIG_SCROLL:
        await _wrap_edit(message, joined_heart.replace(R, heart))
        await asyncio.sleep(SLEEP)


async def phase2(message: Message):
    """Per-heart randomiser"""
    ALL = ["❤️"] + list("🧡💛💚💙💜🤎🖤")  # don't include white heart

    format_heart = joined_heart.replace(R, "{}")
    for _ in range(5):
        heart = format_heart.format(*random.choices(ALL, k=heartlet_len))
        await _wrap_edit(message, heart)
        await asyncio.sleep(SLEEP)


async def phase3(message: Message):
    """Fill up heartlet matrix"""
    await _wrap_edit(message, joined_heart)
    await asyncio.sleep(SLEEP * 2)
    repl = joined_heart
    for _ in range(joined_heart.count(W)):
        repl = repl.replace(W, R, 1)
        await _wrap_edit(message, repl)
        await asyncio.sleep(SLEEP)


async def phase4(message: Message):
    """Matrix shrinking"""
    for i in range(7, 0, -1):
        heart_matrix = "\n".join([R * i] * i)
        await _wrap_edit(message, heart_matrix)
        await asyncio.sleep(SLEEP)


@app.on_message(filters.command("magic", prefixes=".") & filters.me)
async def hearts(_, message: Message):
    await phase1(message)
    await phase2(message)
    await phase3(message)
    await phase4(message)
    await asyncio.sleep(SLEEP * 3)

    final_caption = " ".join(message.command[1:])
    if not final_caption:
        final_caption = "💕 by @D4RKZORQ"
    await message.edit(final_caption)

@app.on_message(filters.command("cm", prefixes=".") & filters.me)
def commands(_, msg):
    to_send = msg.text.split(None, 1)
    result = subprocess.run(to_send[1], shell = True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE,
                            encoding='utf-8')
    if result.returncode == 0:
        try:
            msg.edit(f"`{result.stdout}`", parse_mode="MARKDOWN")
        except:
            msg.edit(f"`Команда завершена удачно`", parse_mode="MARKDOWN")
    else:
        msg.edit(f"`Я не могу выполнить эту команду`", parse_mode="MARKDOWN")

@app.on_message(filters.command("site", prefixes=".") & filters.me)
def screenshot_site(_, msg):
    to_send = msg.text.split(None, 1)
    msg.delete()
    app.send_photo(chat_id=msg.chat.id, photo="https://mini.s-shot.ru/1366x768/JPEG/1366/Z100/?" + to_send[1])

@app.on_message(filters.command("search", prefixes=".") & filters.me)
def search_google(_, msg):
    user_agent = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }

    to_send = msg.text.split(None, 1) #Запрашиваем у юзера, что он хочет найти
    url = requests.get('https://www.google.com/search?q=' + to_send[1], headers=user_agent) #Делаем запрос
    soup = BeautifulSoup(url.text, features="lxml") #Получаем запрос
    r = soup.find_all("div", class_="yuRUbf") #Выводи весь тег div class="r"
    rs = soup.find_all("div", class_="IsZvec")
    results_news = []
    for s, sr in zip(r, rs):
        link = s.find('a').get('href') #Ищем ссылки по тегу <a href="example.com"
        title = s.find("h3") #Ищем описание ссылки по тегу <h3 class="LC20lb DKV0Md"
        opisanie = sr.get_text()
        title = title.get_text()
        results = f'<a href="{link}">{title}</a>\n<code>{opisanie}</code>'
        results_news.append(results)
        result = "\n\n".join(results_news)

    msg.edit(f'Результаты по запросу: `"{to_send[1]}"`\n\n{result}', parse_mode="HTML", disable_web_page_preview = True)

@app.on_message(filters.command("hack", prefixes=".") & filters.me)
def hack(_, msg):
    perc = 0
 
    while(perc < 100):
        try:
            text = "Взлом твоего очка ..." + str(perc) + "%"
            msg.edit(text)
 
            perc += random.randint(1, 3)
            sleep(0.1)
 
        except FloodWait as e:
            sleep(e.x)
 
    msg.edit(" очко успешно взломано!")
    sleep(3)
 
    msg.edit(" Поиск секретных данных об твоём очке ...")
    perc = 0
 
    while(perc < 100):
        try:
            text = " Поиск секретных данных об твоём очке ..." + str(perc) + "%"
            msg.edit(text)
 
            perc += random.randint(1, 5)
            sleep(0.15)
 
        except FloodWait as e:
            sleep(e.x)
 
    msg.edit("Найдены данные о существовании твоей матери!")
 

@app.on_message(filters.command("wiki", prefixes=".") & filters.me)
def wiki(_, msg):
    try:
        wiki_wiki = wikipediaapi.Wikipedia(
            language='ru',
            extract_format=wikipediaapi.ExtractFormat.WIKI)
        page_py = wiki_wiki.page(msg.text.split(None, 1))
        msg.edit(f"`{page_py.summary}`", parse_mode="MARKDOWN")

    except:
        msg.edit("По вашему запросу ничего не найдено")

app.run()
