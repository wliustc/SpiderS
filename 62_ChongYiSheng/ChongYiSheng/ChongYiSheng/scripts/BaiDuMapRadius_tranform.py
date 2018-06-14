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
    return str(_json_obj)


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
    line = json.loads(line)
    content = line
    result = {}
    result['uid'] = get_json_hierarchy(content, ['uid'])
    result['address'] = (get_json_hierarchy(content, ['address']))
    result['name'] = (get_json_hierarchy(content, ['name']))
    result['lat'] = (get_json_hierarchy(content, ['lat']))
    result['lng'] = (get_json_hierarchy(content, ['lng']))
    result['telephone'] = (get_json_hierarchy(content, ['telephone']))
    result['distance'] = (get_json_hierarchy(content, ['distance']))
    result['detail_url'] = (get_json_hierarchy(content, ['detail_url']))

    result['service_rating'] = (get_json_hierarchy(content, ['service_rating']))
    result['environment_rating'] = (get_json_hierarchy(content, ['environment_rating']))
    result['clinic_name'] = (get_json_hierarchy(content, ['clinic_name']))
    result['chong_uid'] = (get_json_hierarchy(content, ['chong_uid']))
    result['city_id'] = (get_json_hierarchy(content, ['city_id']))
    result['write_time'] = (get_json_hierarchy(content, ['write_time']))

    print json.dumps(result)

    
    