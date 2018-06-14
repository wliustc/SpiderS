# coding=utf8
import json
import sys

def parse(line):
    line_json = json.loads(line)
    content = line_json.get('content')
    meta = line_json.get('meta')
    # print content
    # content_json = json.loads(content)
    datas = content.get('datas')
    if datas:
        echarts = datas.get('echarts')
        if echarts:
            echarts = echarts[0]
            channelList = echarts.get('channelList')
            if channelList:
                for channel in channelList:
                    item = {}
                    for key,val in channel.items():

                        item[key] = val
                    print json.dumps(item)

for line in sys.stdin:
    parse(line)