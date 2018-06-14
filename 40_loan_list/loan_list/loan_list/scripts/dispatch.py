#encoding=utf-8
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
                elif type(item) == float:
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
    result.append(content['loan_id'])
    result.append(content['loan_duration'])
    result.append(content['loan_amt'])
    result.append(content['month_expense'])
    result.append(content['month_interest_rate'])
    result.append(content['month_add'])
    result.append(content['dt'])
    result.append(content['city'])
    print "\t".join(format_list(result))
