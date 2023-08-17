import requests
from bs4 import BeautifulSoup
import datetime


def pars_habr(type_news, count):
    list_news = []
    url = None
    if type_news == 'Свежее':
        url = "https://vc.ru/new"
    if type_news == "Популярное":
        url = "https://vc.ru/popular"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_articles = soup.find_all('div',
                                  class_='feed__item l-island-round')
    for index in news_articles[:int(count)]:
        title = index.find('div', class_='content-title content-title--short l-island-a').text.strip()
        url = index.find('a', class_='content-link')['href']
        title = title.replace('\n', '')
        list_news.append({'url': url, 'title': title})
    return list_news


print(pars_habr("Популярное", "3"))
