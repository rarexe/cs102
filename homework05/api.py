import requests
import config

def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):

    """ Выполнить GET-запрос
    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки

    """
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=timeout)
            return response
        except:
            if i == max_retries - 1:
                raise


def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
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

