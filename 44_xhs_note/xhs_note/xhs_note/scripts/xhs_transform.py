# -*- coding: utf-8 -*-
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
                    tmp = tmp.replace('\u0001','')
                    tmp = tmp.replace('\n',' ')
                    tmp = tmp.replace('\t',' ')
                    tmp = tmp.replace('\r',' ')
                    tmp = re.sub(r'[\x01-\x1f]','', tmp)
                    tmp = tmp.strip()
                elif type(item) == int:
                    tmp = str(item)
                elif type(item) == str:
                    tmp = item.encode('utf-8').replace("\u0001",'')
                    tmp = tmp.replace('\n',' ')
                    tmp = re.sub(r'[\x01-\x1f]','', tmp)
                    tmp = tmp.replace('\t',' ')
                    tmp = tmp.replace('\r',' ')
                    tmp = tmp.decode('utf-8').strip()
                else:
                    tmp = item
            result.append(tmp)
    return result

for line in sys.stdin:
    try:
        line = json.loads(line)
	line = line['content']
        result = []
        if line:
            note = json.loads(line['note'])
            lists = json.loads(line['list'])
            #id
            result.append(lists['id'])
            #task_date
            result.append(line['task_date'])
            #oid
            result.append(line['oid'])
            #list
            result.append(line['list'])
            #note
            result.append(line['note'])
            #comments
            if 'comments' in note:
                result.append(note['comments'])
            else:
                result.append(None)
            #category
            if 'category' in note:
                result.append(note['category'])
            else:
                result.append(None)
            #p_time
            times = note.get('time',None)
            result.append("{0}:00".format(times))
            result.append(line['task_date'])
            print "\t".join(format_list(result))
    except:
	print "$$$$$$$$$$$$$ ex"
        pass
