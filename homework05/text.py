import config
import pandas as pd
import requests
import textwrap
import pymorphy2
import string
import emoji
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
morph = pymorphy2.MorphAnalyzer()
from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm
import gensim
from gensim.models.ldamulticore import LdaModel
from gensim.corpora.dictionary import Dictionary
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import matplotlib.colors as mcolors

def get_wall(
        owner_id: str ='',
        domain: str ='',
        offset: int = 0,
        count: int = 10,
        filter: str = 'owner',
        extended: int = 0,
        fields: str = '',
        v: str = '5.103'
):
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """
    code = ("return API.wall.get({" +
            f"'owner_id': '{owner_id}'," +
            f"'domain': '{domain}'," +
            f"'offset': {offset}," +
            f"'count': {count}," +
            f"'filter': '{filter}'," +
            f"'extended': {extended}," +
            f"'fields': '{fields}'," +
            f"'v': {v}," +
            "});")
    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={
            "code": code,
            "access_token": config.VK_CONFIG['access_token'],
            "v": v
        }
    )
    walls = []
    for i in range(count):
        try:
            walls.append(response.json()['response']['items'][i]['text'])
        except:
            break
    return walls


def emoji_free_text(text):
    text = re.sub(emoji.get_emoji_regexp(), r'', text)
    return(text)

def no_stopwords(text):
    stop_words = stopwords.words('russian')
    stoplist = set(stop_words)
    text = word_tokenize(text)
    wordsFiltered = []
    for n in text:
        if n not in stoplist:
            wordsFiltered.append(n)
    return wordsFiltered

def no_links(text):
    text = re.sub(r'https\S+', '', text)
    return text


def delete_symbols(text):
    exclude = set(string.punctuation)
    text = ''.join(ch for ch in text if ch not in exclude)
    for a in '«»-——№':
        text = text.replace(a, '')
    for d in '1234567890':
        text = text.replace(d, '')
    return text


def updated_text(text):
    new_text = emoji_free_text(text)
    new_text = no_links(new_text)
    new_text = delete_symbols(new_text)
    new_text = no_stopwords(new_text)
    new_text = ' '.join(new_text)
    return([morph.parse(n)[0].normal_form for n in new_text.split()])
wall = []
for i in range(1):
	for group in ['animalplanetrussia']:
		wall.extend(get_wall(domain=group, count=100, offset=100))
wall = ' '.join(wall)
wall = updated_text(wall)
print(wall)
new_wall = [w.split() for w in wall]
dictionary = gensim.corpora.Dictionary(new_wall)
corpus = [dictionary.doc2bow(wall)]
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=dictionary,
                                           num_topics=1,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=10,
                                           passes=10,
                                           alpha='symmetric',
                                           iterations=100,
                                           per_word_topics=True)
print(lda_model.print_topics())
cols = [color for name, color in mcolors.TABLEAU_COLORS.items()]
cloud = WordCloud(stopwords=STOPWORDS,
                  background_color='white',
                  width=2500,
                  height=1800,
                  max_words=30,
                  colormap='tab10',
                  color_func=lambda *args, **kwargs: cols[i],
                  prefer_horizontal=1.0)
topics = lda_model.show_topics(formatted=False)
fig, axes = plt.subplots(1,1, figsize=(10,10), sharex=True, sharey=True)

topic_words = dict(topics[0][1])
cloud.generate_from_frequencies(topic_words, max_font_size=300)
plt.gca().imshow(cloud)
plt.gca().set_title('Topic', fontdict=dict(size=16))
plt.gca().axis('off')
plt.subplots_adjust(wspace=0, hspace=0)
plt.axis('off')
plt.margins(x=0, y=0)
plt.tight_layout()
plt.show()


