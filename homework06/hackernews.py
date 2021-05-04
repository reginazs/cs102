import string

from bottle import redirect, request, route, run, template

from bayes import NaiveBayesClassifie
from db import News, session
from scraputils import get_news


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    news_id = request.query.id
    label = request.query.label
    s = session()
    qurent = s.query(News).filter(News.id == news_id).one()
    qurent.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    news = get_news('https://news.ycombinator.com/newest', 1)
    s = session()
    for item in news:
        if s.query(News).filter(News.title == item['title'], News.author == item['author']).first():
            continue
        s.add(News(**item))

    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    def classify_news():
    s = session()
    rows_unlabelled = s.query(News).filter(News.label == None).all()
    X = [clean(row.title).lower() for row in rows_unlabelled]

    predictions = model.predict(X)
    rows_good = [rows_unlabelled[i] for i in range(len(rows_unlabelled)) if predictions[i] == 'good']
    rows_maybe = [rows_unlabelled[i] for i in range(len(rows_unlabelled)) if predictions[i] == 'maybe']
    rows_never = [rows_unlabelled[i] for i in range(len(rows_unlabelled)) if predictions[i] == 'never']

    return template('classify_template', rows_good=rows_good, rows_maybe=rows_maybe, rows_never=rows_never)


if __name__ == "__main__":
    run(host="localhost", port=8080)

