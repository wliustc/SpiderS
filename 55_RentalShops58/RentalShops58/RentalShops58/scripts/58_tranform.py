# -*- encoding:utf-8 -*-
import sys
import json
import re

import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

_mapping = {
    'sellCount': re.compile(r'\\"sellCount\\":\\"(\d+)\\"'),
}


def get_regex_group1(key, _str, default=None):
    p = _mapping[key]
    m = p.search(_str)
    if m:
        return m.group(1)
    return default


def get_json_hierarchy(_json_obj, arch_ele_list):
    for e in arch_ele_list:
        if e not in _json_obj:
            return None
        _json_obj = _json_obj[e]
    return _json_obj


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


def get_brand(content):
    brand_info_list = get_json_hierarchy(content, ['detail', 'eleParameterList'])
    for bd in brand_info_list:
        if bd.has_key(u'主体'):
            brand_name = bd[u'主体'][0]['snparameterVal']
            return brand_name
    return None

def list_to_str(list):
    return json.dumps(list)

uid_set = set()
for line in sys.stdin:
    # print line
    line = json.loads(line)
    content = line
    result = []
    result.append(get_json_hierarchy(content, ['detail_url']))
    result.append(get_json_hierarchy(content, ['city']))
    result.append(get_json_hierarchy(content, ['title']))
    result.append(json.dumps(get_json_hierarchy(content, ['pictures'])))
    result.append(get_json_hierarchy(content, ['region']))
    result.append(get_json_hierarchy(content, ['describe']))

    result.append(get_json_hierarchy(content, ['longitude']))
    result.append(get_json_hierarchy(content, ['approach']))
    result.append(get_json_hierarchy(content, ['rentable_area']))
    pubtime = get_json_hierarchy(content, ['pubtime'])
    if pubtime:
        if len(pubtime) == 7:
            pubtime = pubtime[:2] + datetime.datetime.now().strftime('%Y')[2:4] + '-' + pubtime[2:]
    result.append(pubtime)
    result.append(get_json_hierarchy(content, ['latitude']))

    result.append(get_json_hierarchy(content, ['contact_name']))
    result.append(get_json_hierarchy(content, ['property_type']))
    result.append(get_json_hierarchy(content, ['contact_phone']))
    result.append(get_json_hierarchy(content, ['rent']))
    result.append(get_json_hierarchy(content, ['right_keyword']))
    tasktime = get_json_hierarchy(content, ['tasktime'])
    if not tasktime:
        tasktime = '2017-11-17'
    result.append(tasktime)
    result.append(tasktime)

    print "\t".join(format_list(result))
    # print len(result)