# coding=utf8

import json
import sys

data_class_dic = {
    'node_activeness_count': "分时活跃用户",
    'node_launch_count': "分时启动次数",
    'node_runtime_time': "分时使用时长",
    'node_activeness_averaged_count': "分时人均启动次数",
    'node_activeness_averaged_time': "分时人均使用时长",
    'node_activeness_absolute_permeability': "分时绝对渗透率",
    'node_activeness_relative_permeability': "分时相对渗透率"
}


def parse(line):
    line_json = json.loads(line)
    content = line_json.get('content')
    meta = line_json.get('meta')
    content_json = json.loads(content)
    datas = content_json.get('datas')
    if datas:
        echarts = datas.get('echarts')
        if echarts:
            echarts = echarts[0]
            for echart in echarts:
                if data_class_dic.get(echart):
                    if echarts.get(echart):
                        for ec in echarts.get(echart):
                            ec['data_name'] = data_class_dic.get(echart)
                            for i in xrange(24):
                                ec.pop('value'+str(i))
                            print json.dumps(ec)

for line in sys.stdin:
    parse(line)



