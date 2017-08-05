#!practice/bin/python
# -*- coding:utf-8 -*-

from flask import request
from flask import Flask
import Analyze

app = Flask(__name__)


# 查询成绩路由
@app.route('/api/scoreQuery', methods=['POST'])
def query_score():
    username = request.form.get('username')
    password = request.form.get('password')
    term = request.form.get('term')
    # print username
    # print term
    json_score = Analyze.get_score(username, password, term)
    return json_score


# 查询课表路由
@app.route('/api/scheduleQuery', methods=['POST'])
def query_schedule():
    username = request.form.get('username')
    password = request.form.get('password')
    json_schedule = Analyze.get_schedule(username, password)
    return json_schedule


@app.route('/api/todayScheduleQuery', methods=['POST'])
def query_today_schedule():
    username = request.form.get('username')
    password = request.form.get('password')
    date = request.form.get('date')
    json_today_schedule = Analyze.get_today_schedule(username, password, date)
    return json_today_schedule


if __name__ == '__main__':
    app.run(debug=True)
