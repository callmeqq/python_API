#!/usr/bin/env python
# encoding: utf-8

import requests
import Captcha


# 教务系统登录类
class Login:
    __score_url = 'http://jwxt.ecjtu.jx.cn/scoreQuery/stuScoreQue_getStuScore.action'
    __class_schedule_url = 'http://jwxt.ecjtu.jx.cn/Schedule/Schedule_getUserSchedume.action'
    __jwxt_url = 'http://jwxt.ecjtu.jx.cn/stuMag/Login_login.action'
    __captcha_url = 'http://jwxt.ecjtu.jx.cn/servlet/code.servlet'
    __today_schedule_url = 'http://jwxt.ecjtu.jx.cn/Schedule/Weekcalendar_getTodayWeekcalendar.action'
    __agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    __headers = {'User-Agent': __agent}
    __cookies = {}
    SCORE = 0
    SCHEDULE = 1

    def __init__(self):
        return

    # 获取cookies
    @classmethod
    def __login_jwxt(cls, username, password):

        captcha_response = requests.get(cls.__captcha_url, headers=cls.__headers)
        cls.__cookies = captcha_response.cookies
        code = Captcha.get_captcha(captcha_response)
        jwxt_postdata = {'UserName': username,
                         'Password': password,
                         'code': code
                         }
        response = requests.post(cls.__jwxt_url, data=jwxt_postdata, cookies=cls.__cookies, headers=cls.__headers)
        return response.text

    # 获取html页面
    @classmethod
    def get_html_text(cls, username, password, enum):
        response = cls.__login_jwxt(username, password)
        while response == u'验证码错误':
            response = cls.__login_jwxt(username, password)
        if response != 'success':
            return response
        elif enum == cls.SCORE:
            score_text = requests.get(cls.__score_url, cookies=cls.__cookies, headers=cls.__headers).text
            return score_text
        elif enum == cls.SCHEDULE:
            schedule_text = requests.get(cls.__class_schedule_url, cookies=cls.__cookies, headers=cls.__headers).text
            return schedule_text

    # 获取今日课表json数据
    @classmethod
    def get_today_schedule_data(cls, username, password, date):
        response = cls.__login_jwxt(username, password)
        while response == u'验证码错误':
            response = cls.__login_jwxt(username, password)
        if response != 'success':
            return response
        else:
            post_data = {'date': date,
                        'dataType': "json"}
            data = requests.post(cls.__today_schedule_url, data=post_data, cookies=cls.__cookies,
                                 headers=cls.__headers)
            return data
