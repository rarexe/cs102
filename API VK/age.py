import datetime
from datetime import date
from statistics import median
from typing import Optional
from homework05.api import get_friends
from homework05.api_models import User

def age_predict(user_id: int) -> Optional[float]:

    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, 'bdate')
    cur_year = int(datetime.datetime.today().strftime("%Y"))
    cur_month = int(datetime.datetime.today().strftime("%m"))
    cur_day = int(datetime.datetime.today().strftime("%d"))
    age_list = []
    if friends is not None:
        for friend in friends['response']['items']:
            try:
                day, month, year = map(int, friend['bdate'].split('.'))
                bdate = datetime.datetime(year, month, day)
                f_bd_year = year
                f_bd_month = month
                f_bd_day = day
                if f_bd_month < cur_month:
                    age = cur_year - int(f_bd_year)
                elif f_bd_month == cur_month:
                    if f_bd_day <= cur_day:
                        age = cur_year - int(f_bd_year)
                    else:
                        age = cur_year - int(f_bd_year) - 1
                elif f_bd_month > cur_month:
                    age = cur_year - int(f_bd_year) - 1
                age_list.append(age)
            except:
                pass
        if len(age_list) != 0:
            return median(age_list)
        else:
            return None

if __name__ == '__main__':
    print('Age:', age_predict(423700715))

