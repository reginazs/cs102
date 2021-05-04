from bottle import (route, run, template, request, redirect)
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    row_id = request.query.id
    row = s.query(News).filter(News.id == row_id).one()
    row.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    last_news = get_news()
    for news in last_news:
        check = s.query(News).filter(News.author==news['author'], News.title==news['title']).count()
        if check == 0:
            new = News(title=news['title'], author=news['author'], url=news['url'],
                comments=news['comments'], points=news['points'])
            s.add(new)
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    new_news_lable = s.query(News).filter(News.title not in x_train and News.label != None).all()
    x_train_new = [row.title for row in new_news_lable]
    y_train_new = [row.label for row in new_news_lable]
    classifier.fit(x_train_new, y_train_new)
    news_without_lable = s.query(News).filter(News.label == None).all()
    x = [row.title for row in news_without_lable]
    label = classifier.predict(x)
    classified_news = [[] for _ in range(3)]
    good = [news_without_lable[i] for i in
                    range(len(news_without_lable)) if label[i] == 'good']
    maybe = [news_without_lable[i] for i in
                    range(len(news_without_lable)) if label[i] == 'maybe']
    never = [news_without_lable[i] for i in
                    range(len(news_without_lable)) if label[i] == 'never']

    return template('recommended', {'good': good, 'never': never, 'maybe': maybe})


if __name__ == "__main__":
    s = session()
    classifier = NaiveBayesClassifier()
    marked_news = s.query(News).filter(News.label != None).all()
    x_train = [row.title for row in marked_news]
    y_train = [row.label for row in marked_news]
    classifier.fit(x_train, y_train)
    run(host="localhost", port=8080)
