# -*- coding: utf-8 -*-
import time
import datetime
import re

def time_zh(times):
    if re.findall(':', times):
        date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    elif times == u'发布于昨天':
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        date = today - oneday
    else:
        t = ''.join(re.findall('\d', times))
        if len(t) == 8:
            date = t[0:4]+'-'+t[4:6]+'-'+t[6:]
        else:
            date = time.strftime('%Y-', time.localtime(time.time()))+t[0:2]+'-'+t[2:]
    return date