<<<<<<< HEAD
import string

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template  # type: ignore
from db import News, session
from scraputils import get_news
=======
from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier
>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
<<<<<<< HEAD
    return template("news_template", rows=rows)
=======
    return template('news_template', rows=rows)
>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0


@route("/add_label/")
def add_label():
<<<<<<< HEAD
    query = request.query.decode()
    id = int(query["id"])
    label = query["label"]
    s = session()
    s.query(News).filter(News.id == id).update({News.label: label})
    s.commit()
    redirect("/news")


def has(ses, author, title):
    return (
        len(ses.query(News.author).filter_by(author=author).all()) == 0
        or len(ses.query(News.title).filter_by(title=title).all()) == 0
    )


@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/", 3)
    s = session()
    for n in news:  # n поменять на new
        if has(s, n["author"], n["title"]):
            s.add(
                News(
                    title=n["title"],
                    author=n["author"],
                    url=n["url"],
                    points=n["points"],
                    comments=n["comments"],
                )
            )
    s.commit()
    redirect("/news")


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


@route("/classify")
def classify_news():
    s = session()
    model = NaiveBayesClassifier()
    train_set = s.query(News).filter(News.label != None).all()
    model.fit(
        [clean(news.title).lower() for news in train_set],
        [news.label for news in train_set],
    )
    test = s.query(News).filter(News.label == None).all()
    return template(
        "news_template",
        rows=sorted(
            test, key=lambda news: get_weight(model.predict(clean(news.title).lower()))
        ),
    )


def get_weight(label):
    if label == "never":
        return 2
    elif label == "maybe":
        return 1
    elif label == "good":
        return 0
    else:
        raise AssertionError("Invalid label" + label)
=======
    # PUT YOUR CODE HERE
    redirect("/news")


@route("/update")
def update_news():
    # PUT YOUR CODE HERE
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0


if __name__ == "__main__":
    run(host="localhost", port=8080)
<<<<<<< HEAD
=======

>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0
