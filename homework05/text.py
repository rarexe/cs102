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
import pyLDAvis
import pyLDAvis.gensim

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
    stoplist = set(stopwords.words('russian'))
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
    for a in '«»-–':
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
    print([morph.parse(n)[0].normal_form for n in new_text.split()])


wall = []
for i in range(2):
	for group in ['itmoru','sportsru']:
		wall.extend(get_wall(domain=group, count=100, offset=100*i))
wall = ' '.join(wall)
wall = updated_text(wall)
dictionary = Dictionary(wall)
new_text = []
for i in range(len(wall)):
    new_text.extend(wall[i])
corpus = [dictionary.doc2bow(new_text)]
lda= gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                id2word=dictionary,
                                                num_topics=10,
                                                alpha='auto',
                                                per_word_topics=False)
vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary)
pyLDAvis.save_html(vis, 'LDA.html')
pyLDAvis.show(data = vis, open_browser = True)




