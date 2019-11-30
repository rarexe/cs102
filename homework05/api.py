import requests
import time
import config
def get(url, params=({}), timeout=5, max_retries=5, backoff_factor=1.3):
    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """

    for n in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=(timeout, 3))
            return response
        except requests.exceptions.RequestException:
            if n == max_retries - 1:
                raise
            delay = backoff_factor * 2 ** n
            time.sleep(delay)




def get_friends(user_id, fields=''):
    """" Вернуть данных о друзьях пользователя
    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query = (f"{config.VK_CONFIG['domain']}/" +
             "friends.get?" +
             f"access_token={config.VK_CONFIG['access_token']}&" +
             f"user_id={user_id}&" +
             f"fields={fields}&" +
             f"v={config.VK_CONFIG['version']}")
    response = requests.get(query)

    return response.json()


