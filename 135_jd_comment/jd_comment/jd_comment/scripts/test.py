#-*- encoding:utf-8 -*-
import sys
import json
import re
reload(sys)
sys.setdefaultencoding('utf-8')


_mapping = {
    'sellCount':re.compile(r'\\"sellCount\\":\\"(\d+)\\"'),
}

def get_regex_group1(key,_str, default=None):

    p = _mapping[key]
    m = p.search(_str)
    if m:
        return m.group(1)
    return default

def get_json_hierarchy(_json_obj, arch_ele_list):
    for e in arch_ele_list: #把数据从json的层里扒出来
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
                    tmp = tmp.replace('\u0001','')
                    tmp = tmp.replace('\n',' ')
                    tmp = tmp.replace('\t',' ')
                    tmp = tmp.replace('\r',' ')
                    tmp = tmp.strip()
                elif type(item) == int:
                    tmp = str(item)
                elif type(item) == str:
                    tmp = item.encode('utf-8').replace("\u0001",'')
                    tmp = tmp.replace('\n',' ')
                    tmp = tmp.replace('\t',' ')
                    tmp = tmp.replace('\r',' ')
                    tmp = tmp.decode('utf-8').strip()
                else:
                    tmp = item
            result.append(tmp)
    return result

for line in sys.stdin:
    line = json.loads(line)
    content = line
    result = []
    itemId = get_json_hierarchy(content, ['sku'])
    result.append(itemId)
    result.append(get_json_hierarchy(content, ['brand']))
    result.append(get_json_hierarchy(content, ['comments']))
    result.append(get_json_hierarchy(content, ['comment_type']))
    result.append(get_json_hierarchy(content, ['good_comment_rate']))
    result.append(get_json_hierarchy(content, ['comment_time']))
    result.append(get_json_hierarchy(content, ['comments_name']))
    result.append(get_json_hierarchy(content, ['score']))
    result.append(get_json_hierarchy(content, ['reply']))
    result.append(get_json_hierarchy(content, ['user_id']))
    result.append(get_json_hierarchy(content, ['price']))
    result.append(get_json_hierarchy(content, ['yanse']))
    result.append(get_json_hierarchy(content, ['chicun']))
    result.append(get_json_hierarchy(content, ['dt']))
    shop_name = get_json_hierarchy(content, ['shop_name'])
    result.append(get_json_hierarchy(content, ['comment_id']))
    result.append(shop_name)
    print "\t".join(format_list(result))
    
    
    
    
    
    