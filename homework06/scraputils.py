import requests
<<<<<<< HEAD
from bs4 import BeautifulSoup  # type: ignore
=======
from bs4 import BeautifulSoup
>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0


def extract_news(parser):
    """ Extract news from a given web page """
<<<<<<< HEAD

    def extract_first_integer_from_tag(tag, separator):
        try:
            return 0 if tag is None else int(tag.text.split(separator)[0])
        except ValueError:
            return 0

    news = []

    links = parser.findAll("a", {"class": "storylink"})
    subtexts = parser.findAll("td", {"class": "subtext"})

    for i in range(len(links)):
        author = subtexts[i].find("a", {"class": "hnuser"})
        comments = extract_first_integer_from_tag(subtexts[i].find_all("a")[-1], "\xa0")
        points = extract_first_integer_from_tag(
            subtexts[i].find("span", {"class": "score"}), " "
        )

        news.append(
            {
                "author": None if author is None else author.text,
                "comments": comments,
                "points": points,
                "title": links[i].text,
                "url": links[i]["href"],
            }
        )
    return news
=======
    news_list = []

    # PUT YOUR CODE HERE

    return news_list
>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0


def extract_next_page(parser):
    """ Extract next page URL """
<<<<<<< HEAD
    return parser.find("a", {"class": "morelink"})["href"]
=======
    # PUT YOUR CODE HERE
>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
<<<<<<< HEAD
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        current_news = extract_news(soup)
        next_url = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_url
        news.extend(current_news)
        n_pages -= 1
    return news
=======
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0
