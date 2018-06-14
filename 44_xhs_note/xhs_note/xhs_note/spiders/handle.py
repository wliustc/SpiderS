# -*- coding: utf-8 -*-
import time
import hashlib
import urllib
def get_sign(params_dict):
    keys = params_dict.keys()
    keys.sort()
    mess = ''
    for k in keys:
        mess += k+'='+params_dict[k]
    mess = urllib.quote_plus(mess)

    a = bytearray(mess, encoding='utf-8')
    b = bytearray(params_dict['deviceId'], encoding='utf-8')
    c = ''
    j = 0
    for byt in a:
        c += str(byt^b[j])
        j = (j+1)%len(b)
    return hashlib.md5((hashlib.md5(c).hexdigest() + params_dict['deviceId'])).hexdigest()

def get_time():
    return str(time.time())[:10]
