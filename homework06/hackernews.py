from bottle import (
    route, run, template, request, redirect, TEMPLATE_PATH
)
from homework06.db import News, session
from homework06.scraputils import get_news
from homework06.bayes import NaiveBayesClassifier
from homework06.bayes import  clean


@route("/news")
def news_list():
    TEMPLATE_PATH.insert(0, '')
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)

@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    id = request.query.get('id')
    label = request.query.get('label')
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    s = session()
    entry = s.query(News).get(id)
    # 3. Изменить значение метки записи на значение label
    entry.label = label
    # 4. Сохранить результат в БД
    s.commit()
    redirect("/news")

@route('/update')
def update_news():
    news_s = get_news('https://news.ycombinator.com/newest', n_pages=5)
    s = session()
    news_bd = s.query(News).all()
    news_bd = [(n.title, n.author) for n in news_bd]
    for new in news_s:
        if (new['title'], new['author']) not in news_bd:
            news = News(title=new['title'],
                           author=new['author'],
                           url=new['url'],
                           comments=new['comments'],
                           points=new['points'])
            s.add(news)
            s.commit()
    redirect('/news')

@route('/rec')
def recommendations():
    TEMPLATE_PATH.insert(0, '')
    s = session()
    # 1. Classify labeled news
    rows = s.query(News).filter(News.label != None).all()
    X, y = [], []
    for row in rows:
        X.append(row.title)
        y.append(row.label)
    X = [x for x in X]
    model = NaiveBayesClassifier()
    model.fit(X, y)
    # 2. Get unlabeled news
    new_rows = s.query(News).filter(News.label == None).all()
    # 3. Get predictions
    marked = []
    for row in new_rows:
        marked.append((model.predict(row.title.split()), row))
    # 4. Print ranked table
    return template('news_ranked', rows=marked)

if __name__ == "__main__":
    run(host="localhost", port=8080)
