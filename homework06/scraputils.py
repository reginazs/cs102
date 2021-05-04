import requests
from bs4 import BeautifulSoup
import socket


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    news_list_subtext = []
    news = {}
    try:
        tbl_list_title = parser.table.findAll('a', attrs={"class": "storylink"})
    except AttributeError:
        return news_list
    for link in tbl_list_title:
        news = dict(title=link.get_text(), url=link.get('href'))
        news_list.append(news)
    try:
        tbl_list_subtext = parser.table.findAll('td', attrs={"class": "subtext"})
    except AttributeError:
        return news_list
    for link in tbl_list_subtext:
        news = dict(author=link.find('a', attrs={"class": "hnuser"}).get_text(),
                comments=link.findAll('a')[-1].get_text(),
                points=link.find('span', attrs={"class": "score"}).get_text()[:-6])
        news_list_subtext.append(news)
    for news in news_list_subtext:
        if news['comments'] == 'discuss':
            news['comments'] = '0'
        else:
            news['comments'] = news['comments'][:-9]
        if news['points'][-1] == ' ':
            news['points'] = news['points'][:-1]
    for news in range(len(news_list)):
        news_list[news].update(news_list_subtext[news])

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    try:
        next_page = parser.table.find('a', attrs={"class": "morelink"}).get('href')
    except AttributeError:
        url_ip = "https://news.ycombinator.com/unban?ip=213.21.44.132"
        response_ip = requests.get(url_ip)
        next_page = parser.table.find('a', attrs={"class": "morelink"}).get('href')
    return next_page


def get_news(url='https://news.ycombinator.com/newest', n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        if next_page == "":
            return news
    return news
