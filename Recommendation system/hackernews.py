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
    s = session()
    labeled = s.query(News).filter(News.label != None).all() #новости, которые разметили
    news_title = [news.title for news in labeled]
    news_label = [news.label for news in labeled]
    bayes = NaiveBayesClassifier() #пропускаем данные через наивный классификатор
    bayes.fit(news_title, news_label)
    notlabeled = s.query(News).filter(News.label == None).all() #новости, которые не разметили
    new_news_title = [news.title for news in notlabeled]
    new_news_label = bayes.predict(new_news_title)
    good_news, maybe_news, never_news = [], [], []
    #Добавляем метки нерзамечанным новостям
    for id, label in enumerate(new_news_label):
        if label == 'good':
            good_news.append(notlabeled[id])
        elif label == 'maybe':
            maybe_news.append(notlabeled[id])
        elif label == 'never':
            never_news.append(notlabeled[id])
    classified_news = [good_news, maybe_news, never_news]
    return template('news_ranked', good_news=good_news, maybe_news=maybe_news, never_news=never_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
