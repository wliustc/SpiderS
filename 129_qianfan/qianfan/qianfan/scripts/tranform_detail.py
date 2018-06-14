# coding=utf8

import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def get_json_hierarchy1(_json_obj, arch_ele_list):
    for e in arch_ele_list:
        if e not in _json_obj:
            return None
        _json_obj = _json_obj[str(e)]
    return str(_json_obj)


def get_json_hierarchy(el, _json_obj):
    if _json_obj.get(el):
        return str(_json_obj.get(el))
    else:
        return ''


def format_list(data):
    result = []
    if data:
        for item in data:
            tmp = ''
            if item:
                if type(item) == unicode:
                    tmp = item.encode('utf-8')
                    tmp = tmp.replace('\u0001', '')
                    tmp = tmp.replace('\n', ' ')
                    tmp = tmp.replace('\t', ' ')
                    tmp = tmp.replace('\r', ' ')
                    tmp = tmp.strip()
                elif type(item) == int:
                    tmp = str(item)
                elif type(item) == str:
                    tmp = item.encode('utf-8').replace("\u0001", '')
                    tmp = tmp.replace('\n', ' ')
                    tmp = tmp.replace('\t', ' ')
                    tmp = tmp.replace('\r', ' ')
                    tmp = tmp.decode('utf-8').strip()
                else:
                    tmp = item
            result.append(tmp)
    return result


def parse(line):
    line = json.loads(line)
    content = line.get('content')
    meta = line.get('meta')
    # print meta
    content = json.loads(content)
    datas = content.get('datas')
    if datas:
        echarts = datas.get('echarts')
        if echarts:
            echarts = echarts[0]
            indexList = echarts.get('indexList')
            if indexList:
                for echart in indexList:
                    result = []
                    if get_json_hierarchy('appId', echart):
                        result.append(meta.get('url'))
                        result.append('')
                        result.append(meta.get('date_class')[1])
                        result.append(get_json_hierarchy('launchNumsPercent', echart))
                        result.append(get_json_hierarchy('activeNums', echart))
                        result.append(get_json_hierarchy('arithId', echart))
                        result.append(get_json_hierarchy('arithName', echart))
                        result.append(get_json_hierarchy('activeAbsolutePermeabilityRate', echart))
                        result.append(get_json_hierarchy('cateName', echart))
                        result.append(get_json_hierarchy('launchNums', echart))
                        result.append(get_json_hierarchy('appId', echart))
                        result.append(get_json_hierarchy('activeRelativePermeabilityRate', echart))
                        result.append(get_json_hierarchy('runtimeNums', echart))
                        result.append(get_json_hierarchy('statDate', echart))
                        result.append(get_json_hierarchy('appName', echart))
                        result.append(get_json_hierarchy('isDisplay', echart))
                        result.append(get_json_hierarchy('runtimeNumsRatio', echart))
                        result.append(get_json_hierarchy('companyId', echart))
                        result.append(get_json_hierarchy('companyAbbrName', echart))
                        result.append(get_json_hierarchy('createdDate', echart))
                        result.append(get_json_hierarchy('echartX', echart))
                        result.append(get_json_hierarchy('cateId', echart))
                        result.append(get_json_hierarchy('activeNumsRatio', echart))
                        result.append(get_json_hierarchy('launchNumsRatio', echart))
                        result.append(get_json_hierarchy('status', echart))
                        result.append(meta.get('dt'))
                        print '\t'.join(format_list(result))


for line in sys.stdin:
    parse(line)




