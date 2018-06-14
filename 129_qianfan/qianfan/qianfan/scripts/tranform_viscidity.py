# coding=utf8

import json
import sys

data_class_dic = {'runtime_avg_person': "人均单日使用时长（月度）",
                  'launch_avg_person': "人均单日启动次数（月度）",
                  'activeness': "用户活跃度",
                  'retained_rate': "次月留存率",
                  'launch_per_person': "人均启动次数（月度）",
                  'runtime_per_person': "人均使用时长（月度）"}

data_class = ['runtime_avg_person', 'launch_avg_person', 'activeness',
              'launch_per_person', 'runtime_per_person']


def extract(index):
    ex_ll = ['retainedRate', 'runtimeAvgPerson', 'launchAvgPerson', 'activeness','launchPerPerson','runtimePerPerson']
    for ex in ex_ll:
        if index.get(ex):
            data = index.get(ex)
            data_percent = index.get(ex + 'Percent')
            index.pop(ex)
            index.pop(ex + 'Percent')
            index['data_class'] = ex
            index['data_class_data'] = data
            index['data_percent_class'] = ex + 'Percent'
            index['data_percent_class_data'] = data_percent
            print json.dumps(index)


            # retainedRate
            # retainedRatePercent
            # runtimeAvgPerson
            # runtimeAvgPersonPercent
            # launchAvgPerson
            # launchAvgPersonPercent
            # activenessPercent
            # activeness


def parse(line):
    line_json = json.loads(line)
    content = line_json.get('content')
    content_json = json.loads(content)
    datas = content_json.get('datas')
    if datas:
        echarts = datas.get('echarts')
        if echarts:
            echarts = echarts[0]
            indexList = echarts.get('indexList')
            if indexList:
                for index in indexList:
                    if index in data_class:
                        if indexList.get(index):
                            for ii in indexList.get(index):
                                ii['data_name'] = data_class_dic.get(index)
                                extract(ii)
                    else:
                        index['data_name'] = data_class_dic.get('retained_rate')
                        extract(index)


for line in sys.stdin:
    parse(line)
