# -*- encoding:utf-8 -*-
import sys
import json
import re

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

uid_set = set()
for line in sys.stdin:
    line = json.loads(line)
    content = line
    result = []
    result.append(json.dumps(get_json_hierarchy(content, ['data'])))
    result.append(get_json_hierarchy(content, ['dt']))


    print "\t".join(format_list(result))
    