import datetime
import requests
from statistics import median
from typing import Optional
import config
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
    cur_year = int(datetime.datetime.today().strftime("%Y"))
    cur_month = int(datetime.datetime.today().strftime("%m"))
    cur_day = int(datetime.datetime.today().strftime("%d"))
    friends = get_friends(user_id, 'bdate')
    friends = [User(**f) for f in friends]
    age_list = []
    for f in friends:
        if f.bdate is not None:
            if len(f.bdate) == 2:
                pass
            if len(f.bdate) == 3:
                f_bd = f.bdate.split(".")
                f_bd_year = int(f_bd[2])
                f_bd_month = int(f_bd[1])
                f_bd_day = int(f_bd[0])
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
        else:
            pass
    if age_list:
        return float(median(age_list))

