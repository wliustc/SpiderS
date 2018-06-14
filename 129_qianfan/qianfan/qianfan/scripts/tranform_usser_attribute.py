# coding=utf8
import json
import sys
# import web
user_attribute = {'11000': "性别分布", '21000': "年龄分布", '31000': "消费能力分布", '41000': "地域城市级别分布", '51000': "地域省份分布",'61000': "运营商分布", '71000': "品牌分布", '81000': "地域城市详细分布"}
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


def parse(line):
    line_json = json.loads(line)
    content = line_json.get('content')
    meta = line_json.get('meta')
    print meta
    content_json = json.loads(content)
    datas = content_json.get('datas')
    if datas:
        echarts = datas.get('echarts')
        if echarts:
            echarts = echarts[0]
            item ={}
            # item['appname'] = echarts.get('appName')
            item['appId'] = echarts.get('appId')
            for key,val in user_attribute.items():
                echarts_child = echarts.get(key)
                item['cate'] = val
                for echart_child in echarts_child:
                    for echart_child_key,echart_child_val in echart_child.items():
                        if echart_child_val == 'null':
                            echart_child_val=''
                        item[echart_child_key] = echart_child_val
                    print json.dumps(item)
                    # db.insert('t_spider_qianfan_user_attribute',**item)



for line in sys.stdin:
    parse(line)