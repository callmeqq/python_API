#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
from login import Login
import json


# 获取成绩，返回json数据
def get_score(username, password, term):
    score_text = Login.get_html_text(username, password, Login.SCORE)
    if score_text == u'用户名或密码错误':
        return score_text
    soup = BeautifulSoup(score_text, "html.parser")
    json_data = []
    for item in soup.find_all('ul', class_=term + " term_score"):
        json_info = {}
        score = item.find_all('li')
        # json_info['term'] = score[0].string
        json_info['classname'] = score[1].string
        json_info['demand'] = score[2].string
        json_info['mode'] = score[3].string
        json_info['credit'] = score[4].string
        json_info['score1'] = score[5].string
        json_info['score2'] = score[6].string
        json_info['score3'] = score[7].string
        # print score
        json_data.append(json_info)
    # print json_data
    return json.dumps(json_data)


#
def __get_table_strings(obj):
    table_strings = []
    for item in obj:
        table_strings.append(item)
    return table_strings


def get_schedule(username, password):
    schedule_text = Login.get_html_text(username, password, Login.SCHEDULE)
    if schedule_text == u'用户名或密码错误':
        return schedule_text
    soup = BeautifulSoup(schedule_text, "html.parser")
    json_data = []
    table_data = soup.find_all('td')
    for table_column in range(1, 8):
        json_info = {}
        json_info['weekday'] = __get_table_strings(table_data[table_column + 8 * 0].strings)
        json_info['1-2'] = __get_table_strings(table_data[table_column + 8 * 1].strings)
        json_info['3-4'] = __get_table_strings(table_data[table_column + 8 * 2].strings)
        json_info['5-6'] = __get_table_strings(table_data[table_column + 8 * 3].strings)
        json_info['7-8'] = __get_table_strings(table_data[table_column + 8 * 4].strings)
        json_info['9-10'] = __get_table_strings(table_data[table_column + 8 * 5].strings)
        json_info['11-12'] = __get_table_strings(table_data[table_column + 8 * 6].strings)
        json_data.append(json_info)

    return json.dumps(json_data)


def get_today_schedule(username, password, date):
    schedule_data = Login.get_today_schedule_data(username, password, date)
    if schedule_data == u'用户名或密码错误':
        return schedule_data
    # print schedule_data.text
    data = json.loads(schedule_data.text)
    # print data['weekcalendarpojoList']
    return json.dumps(data['weekcalendarpojoList'])
