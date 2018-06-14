# coding=utf8
import sys
import json
import sys
import web
import time


db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')

category_type_dic = {
    'synthesize': 'p_synthesize',
    'user': 'p_user',
    'channel': 'p_channel',
    'time_share': 'p_time_share'
}

time_share_dic = {
    'node_runtime_time':'分时使用时长',
    'node_launch_count':'分时启动次数',
    'node_activeness_count':'分时活跃人数',
}


class parse_all(object):

    def __init__(self):
        pass

    def stamp_date(self,stamp):
        return time.strftime('%Y-%m-%d',time.localtime(stamp/1000))

    # 采集综合数据
    def p_synthesize(self, item):
        item_json = json.loads(item)
        content = item_json.get('content')
        if content:
            conten_json = json.loads(content)
            datas = conten_json.get('datas')
            if datas:
                indexInfo = datas.get('indexInfo')
                if indexInfo:
                    indexInfo = indexInfo[0]
                    result = {}
                    # 活跃人数
                    activeNums = indexInfo.get('activeNums')
                    result['activeNums'] = activeNums
                    # 启动次数
                    launchNums = indexInfo.get('launchNums')
                    result['launchNums'] = launchNums
                    # 使用时长
                    runtimeNums = indexInfo.get('runtimeNums')
                    result['runtimeNums'] = runtimeNums
                    # 人均启动次数
                    launchPerPerson = indexInfo.get('launchPerPerson')
                    result['launchPerPerson'] = launchPerPerson
                    # 人均使用时长
                    runtimePerPerson = indexInfo.get('runtimePerPerson')
                    result['runtimePerPerson'] = runtimePerPerson
                    # 日均活跃人数
                    activeAvgDay = indexInfo.get('activeAvgDay')
                    result['activeAvgDay'] = activeAvgDay
                    # 日均启动次数
                    launchAvgDay = indexInfo.get('launchAvgDay')
                    result['launchAvgDay'] = launchAvgDay
                    # 日均使用时长
                    runtimeAvgDay = indexInfo.get('runtimeAvgDay')
                    result['runtimeAvgDay'] = runtimeAvgDay
                    # 人均单日启动次数
                    launchAvgPerson = indexInfo.get('launchAvgPerson')
                    result['launchAvgPerson'] = launchAvgPerson
                    # 人均单日使用时长
                    runtimeAvgPerson = indexInfo.get('runtimeAvgPerson')
                    result['runtimeAvgPerson'] = runtimeAvgPerson
                    # 用户活跃度
                    activeness = indexInfo.get('activeness')
                    result['activeness'] = activeness
                    # 次月留存率
                    retainedRate = indexInfo.get('retainedRate')
                    result['retainedRate'] = retainedRate
                    # app相对活跃用户渗透率
                    activeRelativePermeabilityRate = indexInfo.get('activeRelativePermeabilityRate')
                    result['activeRelativePermeabilityRate'] = activeRelativePermeabilityRate
                    # app绝对活跃用户渗透率
                    activeAbsolutePermeabilityRate = indexInfo.get('activeAbsolutePermeabilityRate')
                    result['activeAbsolutePermeabilityRate'] = activeAbsolutePermeabilityRate
                    # 日期
                    statDate = indexInfo.get('statDate')
                    result['statDate'] = statDate
                    appId = indexInfo.get('appId')
                    result['appId'] = appId
                    appName = indexInfo.get('appName')
                    result['appName'] = appName
                    # print result
                    # print statDate
                    db.insert('t_spider_qianfan_customization_synthesize', **result)

    # 采集用户分布（性别分布，年龄分布，消费能力分布，地域分布，设备分布）
    def p_user(self, item):
        item_json = json.loads(item)
        content = item_json.get('content')
        if content:
            conten_json = json.loads(content)
            datas = conten_json.get('datas')
            if datas:
                echarts = datas.get('echarts')
                if echarts:
                    echarts = echarts[0]
                    for echart,vals in echarts.items():
                        if '000' in echart:
                            for val in vals:
                                # print val
                                statDate = val.get('statDate')
                                # 简介内容
                                profileName = val.get('profileName')
                                # 简介分
                                activeNums = val.get('activeNums')
                                # 环比
                                activeNumsRatio = val.get('activeNumsRatio')
                                appId = val.get('appId')
                                appName = val.get('appName')
                                result = {}
                                result['statDate'] = self.stamp_date(statDate)
                                result['profileName'] = profileName
                                result['activeNums'] = activeNums
                                result['activeNumsRatio'] = activeNumsRatio
                                result['appId'] = appId
                                result['appName'] = appName
                                db.insert('t_spider_qianfan_customization_user', **result)
                                # print result


    # 采集app渠道分布
    def p_channel(self, item):
        item_json = json.loads(item)
        content = item_json.get('content')
        if content:
            conten_json = json.loads(content)
            datas = conten_json.get('datas')
            if datas:
                echarts = datas.get('echarts')
                if echarts:
                    echarts = echarts[0]
                    channelList = echarts.get('channelList')
                    if channelList:
                        for channel in channelList:
                            statDate = channel.get('statDate')
                            appId = channel.get('appId')
                            # 渠道分数
                            activeNums = channel.get('activeNums')
                            channelName = channel.get('channelName')
                            result = {}
                            result['statDate'] = self.stamp_date(statDate)
                            result['appId'] = appId
                            result['activeNums'] = activeNums
                            result['channelName'] = channelName
                            db.insert('t_spider_qianfan_customization_channel', **result)
                            # print result

    # 采集分时活跃人数，分时启动次数，分时使用时长
    def p_time_share(self, item):
        item_json = json.loads(item)
        content = item_json.get('content')
        if content:
            conten_json = json.loads(content)
            datas = conten_json.get('datas')
            if datas:
                echarts = datas.get('echarts')
                if echarts:
                    echarts = echarts[0]
                    for key,vals in echarts.items():
                        if vals:
                            for val in vals:
                                if key in time_share_dic:
                                    result = {}
                                    statDate = val.get('statDate')
                                    appId = val.get('appId')
                                    indexName = val.get('indexName')
                                    category_name = time_share_dic.get(indexName)
                                    value = val.get('value')
                                    name = val.get('name')
                                    result['statDate'] = self.stamp_date(statDate)
                                    result['appId'] = appId
                                    result['category_name'] = category_name
                                    result['value'] = value
                                    result['start_time'] = name
                                    # print result
                                    db.insert('t_spider_qianfan_customization_time_share',**result)


def parse(line):
    line_json = json.loads(line)
    category_type = line_json.get('category_type')
    # print category_type_dic.get(category_type)
    pa = parse_all()
    apply(getattr(pa, category_type_dic.get(category_type)), (line,))


for line in sys.stdin:
    parse(line)
