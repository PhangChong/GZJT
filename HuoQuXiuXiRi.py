import json
import random

import requests

dataTime = str(random.random())
my_work = []
my_week = []
my_holiday = []


def get_start(x_year, x_month):
    x_year = str(x_year)
    x_month = str(x_month)
    calculation_month = ["2", "5", "8", "11"]
    for one_month in calculation_month:
        get_work_week_holiday(x_year, one_month, x_month)
    # print('##############以下为国家法定节假日（含调休）、周末休息日##########################')
    # print(my_holiday)
    # print('##############以下为上班日（含补班）##########################')
    # print(my_work)
    # print("工作日天数", len(my_work))


def get_calendar_data(calculation_year, month):
    header = {
        "Content-Type": "application/json;charset=UTF-8"
    }
    param = {
        "query": calculation_year + "年" + month + "月",
        "resource_id": "52109",
        "apiType": "yearMonthData",
        "type": "json",
        "tn": "reserved_all_res_tn",
        "cb": ""
    }
    r = requests.get(url="https://opendata.baidu.com/data/inner",
                     headers=header, params=param).text
    return json.loads(r)["Result"][0]["DisplayData"]["resultData"]["tplData"]["data"]["almanac"]


# 周末和法定假日合并
def get_work_week_holiday(calculation_year, month, value_month):
    # 提取almanac信息
    month_data = get_calendar_data(calculation_year, month)

    for one in month_data:
        # 非周末 且 无status 为正常工作日，记作：0
        if (one["cnDay"] != '日' and one["cnDay"] != '六') and 'status' not in one:
            if one['month'] == value_month:
                v = int(one['day'])
                my_work.append(v)
        # 周末 且 status=2（补班） 为周末补班，记作：2
        elif (one["cnDay"] == '日' or one["cnDay"] == '六') and ('status' in one and one["status"] == '2'):
            if one['month'] == value_month:
                v = int(one['day'])
                my_work.append(v)

        # 周末 且 无status 为正常周末休息，记作：1
        elif (one["cnDay"] == '日' or one["cnDay"] == '六') and 'status' not in one:
            if one['month'] == value_month:
                # v = datetime.date(int(one['year']), int(one['month']), int(one['day']))
                v = int(one['day'])
                my_holiday.append(v)
        # status=1（节假日） 为节假日休息，记作：3
        elif 'status' in one and one["status"] == '1':
            if one['month'] == value_month:
                v = int(one['day'])
                my_holiday.append(v)


if __name__ == '__main__':
    get_start(2024, 1)
