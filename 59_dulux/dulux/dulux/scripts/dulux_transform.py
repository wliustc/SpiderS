import sys
import json


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
    print line
    