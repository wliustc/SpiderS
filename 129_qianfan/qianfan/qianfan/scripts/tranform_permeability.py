# coding=utf8

import sys
import json

data_class_dic = {
    'active_absolute_permeability_rate': "绝对活跃用户渗透率",
    'active_relative_permeability_rate': "相对活跃用户渗透率"
}

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
                    print json.dumps(index)

for line in sys.stdin:
    parse(line)