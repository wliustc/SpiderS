# coding=utf8
import sys
import web, json

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


def parse(line):
    # print line
    db.multiple_insert('t_spider_12306_train', line)
    # db.insert('t_spider_12306_train', **line)

ll = []
lll = []
for line in sys.stdin:
    line = json.loads(line)
    if 'start_station_name' in line:
        if len(lll) < 1000:
            lll.append(line)
        else:
            parse(lll)
            lll = []
    else:
        if len(ll) < 1000:
            ll.append(line)
        else:
            parse(ll)
            ll = []
    # parse(json.loads(line))
parse(ll)
parse(lll)

