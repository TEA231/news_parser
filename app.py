from aiogram import types, executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher import FSMContext
import datetime
import requests
from bs4 import BeautifulSoup
# aiogram, bs4, requests


storage = MemoryStorage()
bot = Bot("TOKEN")
app = Dispatcher(bot, storage=MemoryStorage())


class ProfileStatesGroup(StatesGroup):
    site = State()
    day = State()
    time = State()


async def on_startup(_):
    print('Бот был успешно запущен!')


def get_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('/news'))
    return kb


@app.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Здраствуйте, нажмите /news для продолжения.",
                         reply_markup=get_kb())


@app.message_handler(commands=['news'])
async def site(message: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('habr'))
    kb.add(KeyboardButton('VS'))
    await message.reply("Выберите новостной сайт", reply_markup=kb)
    await ProfileStatesGroup.site.set()


@app.message_handler(state=ProfileStatesGroup.site)
async def load_site(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['site'] = message.text
    if data['site'] == 'habr':
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Сегодня'))
        kb.add(KeyboardButton('Вчера'))
        await message.reply('Выберите за какой день.', reply_markup=kb)
    elif data['site'] == 'VS':
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Популярное'))
        kb.add(KeyboardButton('Свежее'))
        await message.reply('Выберите раздел', reply_markup=kb)

    await ProfileStatesGroup.next()


@app.message_handler(state=ProfileStatesGroup.day)
async def load_day(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['day'] = message.text
    if data['site'] == 'habr':
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('Первые три новости'))
        kb.add(KeyboardButton('01:00-02:00'))
        kb.add(KeyboardButton('02:00-03:00'))
        kb.add(KeyboardButton('03:00-04:00:'))
        kb.add(KeyboardButton('04:00-05:00'))
        kb.add(KeyboardButton('05:00-06:00'))
        kb.add(KeyboardButton('06:00-07:00'))
        kb.add(KeyboardButton('07:00-08:00'))
        kb.add(KeyboardButton('08:00-09:00'))
        kb.add(KeyboardButton('09:00-10:00'))
        kb.add(KeyboardButton('10:00-11:00'))
        kb.add(KeyboardButton('11:00-12:00'))
        kb.add(KeyboardButton('12:00-13:00'))
        kb.add(KeyboardButton('13:00-14:00'))
        kb.add(KeyboardButton('14:00:15:00'))
        kb.add(KeyboardButton('15:00:16:00'))
        kb.add(KeyboardButton('16:00-17:00'))
        kb.add(KeyboardButton('17:00-18:00'))
        kb.add(KeyboardButton('18:00-19:00'))
        kb.add(KeyboardButton('19:00-20:00'))
        kb.add(KeyboardButton('20:00-21:00'))
        kb.add(KeyboardButton('21:00-22:00'))
        kb.add(KeyboardButton('22:00-23:00'))
        kb.add(KeyboardButton('23:00-00:00'))
        kb.add(KeyboardButton('00:00-01:00'))
        await message.reply('Выберите время', reply_markup=kb)
    if data['site'] == 'VS':
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(KeyboardButton('3'))
        kb.add(KeyboardButton('6'))
        await message.reply('Выберите колличество новостей', reply_markup=kb)
    await ProfileStatesGroup.next()


@app.message_handler(state=ProfileStatesGroup.time)
async def load_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text

    await message.reply('Обрабатываем запрос...')
    await state.finish()
    if data['site'] == 'habr':
        time1 = data['time']
        day = data['day']
        list_news1 = None
        if time1 != 'Первые три новости':
            today = datetime.date.today()
            data_pass = None
            if day == 'Сегодня':
                data_pass = today
            elif day == 'Вчера':
                data_pass = today - datetime.timedelta(days=1)

            list_news = []
            url = 'https://habr.com/ru/news/'
            list_page = ['https://habr.com/ru/news/page1/', 'https://habr.com/ru/news/page4/',
                         'https://habr.com/ru/news/page2/', 'https://habr.com/ru/news/page5/',
                         'https://habr.com/ru/news/page3/', ]
            for index in list_page:
                response = requests.get(index)

                soup = BeautifulSoup(response.content, 'html.parser')

                news_articles = soup.find_all('article', class_='tm-articles-list__item')
                for article in news_articles:
                    time_str = str(article.find('time').get('title'))  # получаем дату и время создания статьи
                    time_str, time_str_day = time_str.split(', ')[1].split(':')[0], time_str.split(', ')[0]
                    date_new = datetime.datetime.strptime(time_str_day, "%Y-%m-%d").date()
                    if (int(time_str) >= int(time1.split(':')[0])) and (
                            int(time_str) < int(time1.split('-')[1].split(':')[0])) and date_new == data_pass:
                        title = article.find('h2', class_='tm-title tm-title_h2').text

                        url_news = article.find('a', class_='tm-title__link')['href']

                        list_news.append({'title': title, 'url_news': ('https://habr.com' + url_news)})
            list_news1 = list_news
        elif time1 == 'Первые три новости':
            list_news = []
            url = 'https://habr.com/ru/news/'
            response = requests.get(url)

            soup = BeautifulSoup(response.content, 'html.parser')

            news_articles = soup.find_all('article', class_='tm-articles-list__item')
            for article in news_articles:
                title = article.find('h2', class_='tm-title tm-title_h2').text

                url_news = article.find('a', class_='tm-title__link')['href']

                list_news.append({'title': title, 'url_news': ('https://habr.com' + url_news)})
                if len(list_news) == 3:
                    break
            list_news1 = list_news
        if len(list_news1) != 0:
            for index in list_news1:
                await message.answer(f"""
{index['title']}
{index['url_news']}
""")
        else:
            await message.answer("к сожалению новости отсутствуют.")
    elif data['site'] == 'VS':
        list_news = []
        url = None
        if data['day'] == 'Свежее':
            url = "https://vc.ru/new"
        if data['day'] == "Популярное":
            url = "https://vc.ru/popular"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        news_articles = soup.find_all('div',
                                      class_='feed__item l-island-round')
        for index in news_articles[:int(data['time'])]:
            title = index.find('div', class_='content-title content-title--short l-island-a').text.strip()
            url = index.find('a', class_='content-link')['href']
            title = title.replace('\n', '')
            list_news.append({'url': url, 'title': title})
        for index in list_news:
            await message.answer(f"""
{index['title']}
{index['url']}
""")

    await message.answer("нажмите /news для продолжения.",
                         reply_markup=get_kb())


if __name__ == '__main__':
    executor.start_polling(app, skip_updates=True, on_startup=on_startup)
