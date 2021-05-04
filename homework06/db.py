<<<<<<< HEAD
from scraputils import get_news
from sqlalchemy import Column, Integer, String, create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

Base = declarative_base()  # type: ignore
engine = create_engine("sqlite:///news.db")  # type: ignore
session = sessionmaker(bind=engine)  # type: ignore


class News(Base):  # type: ignore
    __tablename__ = "news"  # type: ignore
=======
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

<<<<<<< HEAD

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    s = session()
    news_list = get_news("https://news.ycombinator.com/newest", n_pages=35)
    for i in range(len(news_list)):
        news = News(
            title=news_list[i]["title"],
            author=news_list[i]["author"],
            url=news_list[i]["url"],
            comments=news_list[i]["comments"],
            points=news_list[i]["points"],
        )
        s.add(news)
        s.commit()
=======
Base.metadata.create_all(bind=engine)
>>>>>>> 54726b53e165737f0c95d8eec927bb6e81b5d2c0
