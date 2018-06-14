# coding=utf8

import sys
import json

data_class_dic = {
    'runtimeAvgDay':"日均使用时长（月度）",
    'launchAvgDay':"日均启动次数（月度）",
    'activeAvgDay':"日均活跃人数（月度）"
}

def extract(index):
    for dd in data_class_dic:
        # print dd
        if index.get(dd):
            index.pop(dd)
            index.pop(dd+'Percent')
            index['data_name'] = data_class_dic.get(dd)
            print json.dumps(index)
            break

def parse(line):
    line_json = json.loads(line)
    content = line_json.get('content')
    content = json.loads(content)
    datas = content.get('datas')
    if datas:
        echarts = datas.get('echarts')
        if echarts:
            echarts = echarts[0]
            indexList = echarts.get('indexList')
            if indexList:
                for index in indexList:
                    if indexList.get(index):
                        for index_val in indexList.get(index):
                            extract(index_val)

for line in sys.stdin:
    parse(line)