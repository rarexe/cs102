import telebot
from telebot import apihelper
import config
import requests
import datetime
from bs4 import BeautifulSoup

bot = telebot.TeleBot(config.access_token)
apihelper.proxy = {'https': 'https://51.15.120.43:3128'}

day_list = ['monday',  'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
day_rus = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_monday(web_page: list, day: str):
    soup = BeautifulSoup(web_page, "html5lib")
    day_num = str(day_list.index(day) + 1) + 'day'

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day_num})

    # Время проведения занятий
    try:
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
    except AttributeError:
        return None
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'])
def get_shedule(message):
    """ Получить расписание на указанный день """
    try:
        day, week, group = message.text.split()
        web_page = get_page(group, week)
        times_lst, locations_lst, lessons_lst = parse_schedule_for_a_monday(web_page, day[1:])
        schedule = parse_schedule_for_a_monday(web_page, day[1:])
        resp = ''
        if schedule is None:
            resp += 'В этот день занятий нет!'
        else:
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except ValueError:
        resp = 'Данные введены неверно. Напишите день недели, номер недели(1-четная, 2- нечетная, 0- общее расписание) и номер группы.'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')

@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    today = int(datetime.date.today().strftime('%w')) - 1
    week = int(datetime.date.today().strftime('%U')) % 2 + 1
    if today == 6:
        today = 0
        week += 1
    else:
        today += 1
    web_page = get_page(group, week)
    schedule = parse_schedule_for_a_monday(web_page, day_list[today])
    if schedule is None:
        resp = 'В этот день занятий нет!'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
    else:
        times_lst, locations_lst, lessons_lst = schedule
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b> {} {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    try:
        _, week, group = message.text.split()
        web_page = get_page(group, week)
        for day in range(7):
            schedule = parse_schedule_for_a_monday(web_page, day_list[day])
            resp = '\n' + '\n' + "<b>{}:</b>".format(day_rus[day]) + '\n' + '\n'
            if schedule is None:
                resp += 'В этот день нет занятий'
            else:
                times_lst, locations_lst, lessons_lst = schedule
                for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}</b>,\n {}, {}\n'.format(time, location, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
    except ValueError:
        resp = 'Данные введены неверно. Напишите команду, номер недели (1 - четная, 2- нечетная, 0- четная/нечетная) и номер группы.'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _, group = message.text.split()
    today = int(datetime.datetime.today().strftime("%w")) - 1
    week = int(datetime.datetime.today().strftime("%U")) % 2 + 1
    web_page = get_page(group, week)
    schedule = parse_schedule_for_a_monday(web_page, day_list[today])
    resp = ''
    if schedule is None:
        a = 0
        while a == 0:
            if today == 6:
                today = 0
                week += 1
            else:
                today += 1
            web_page = get_page(group, week)
            next_schedule = parse_schedule_for_a_monday(web_page, day_list[today])
            if next_schedule is not None:
                times_lst, locations_lst, lessons_lst = parse_schedule_for_a_monday(web_page, day_list[today])
                for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                    resp += '<b>{}\n{}</b> {} {}\n'.format(day_rus[today], time, location,  lesson)
                a = 1
    else:
        cur_hour = int(datetime.datetime.today().strftime('%H'))
        cur_minute = int(datetime.datetime.today().strftime('%M'))
        times_lst, locations_lst, lessons_lst = schedule
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            hour_begin = int(time[0:2])
            minute_begin = int(time[3:5])
            if cur_hour == hour_begin:
                if minute_begin > cur_minute:
                    resp += '<b>{}\n{}</b> {} {}\n'.format(day_rus[today], time, location,  lesson)
            elif cur_hour < hour_begin:
                resp += '<b>{}\n{}</b> {} {}\n'.format(day_rus[today], time, location,  lesson)
            else:
                b = 0
                while b == 0:
                    if today == 5:
                        today = 0
                        week += 1
                    elif today == 6:
                        today = 0
                        week += 1
                    else:
                        today += 1
                    web_page = get_page(group, week)
                    next_schedule = parse_schedule_for_a_monday(web_page, day_list[today])
                    if next_schedule is not None:
                        times_lst, locations_lst, lessons_lst = next_schedule
                        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                            resp += '<b>{}\n{}</b>, {}, {}\n'.format(day_rus[today], time, location,  lesson)
                        b = 1
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
