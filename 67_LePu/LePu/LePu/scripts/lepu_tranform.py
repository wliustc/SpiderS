# -*- coding: utf-8 -*-
# import time
import sys

import time

import datetime
from scrapy.selector import Selector
import re, json
import sys
reload(sys)
sys.setdefaultencoding('utf8')


#     time.sleep(100)
# data = ''.join(open('test.html').readlines())
# # print data

def pick_data(data):
    shop_id = ''.join(re.findall(u'商铺编号：(.*?)<', data))
    title = ''.join(re.findall('<title>(.*?)</title>', data))
    rent = ''.join(re.findall(u'"month"><em>(.*?)</em>元/月</span>', data))
    region = ''.join(re.findall(u'区</i>县：</span>(.*?)</p>', data))
    commercial_district = ''.join(re.findall(u'商</i>圈：</span>(.*?)</p>', data))
    street = ''.join(re.findall(u'街</i>道：</span>(.*?)</p>', data))
    update_time = ''.join(re.findall('fr time">(.*?)</span></p', data))


# with open('lepuresult.json') as f:
#     data=f.readlines()
# for d in data:
#     d = json.loads(d)
#     d = d['content']
#     pick_data(d)

def tranform_pubtime(pubtime):
    # pubtime =pubtime.replace('发布：','')
    if '天前' in pubtime:
        pubtime = int(pubtime.replace('天前更新', ''))
        pubtime = datetime.datetime.now() + datetime.timedelta(days=-pubtime)
        pubtime = pubtime.strftime('%Y-%m-%d')
    elif '小时前' in pubtime:
        pubtime = int(pubtime.replace('小时前更新', ''))
        pubtime = datetime.datetime.now() + datetime.timedelta(hours=-pubtime)
        pubtime = pubtime.strftime('%Y-%m-%d')
    elif '分钟前' in pubtime:
        pubtime = int(pubtime.replace('分钟前更新', ''))
        pubtime = datetime.datetime.now() + datetime.timedelta(minutes=-pubtime)
        pubtime = pubtime.strftime('%Y-%m-%d')
    elif '刚刚' in pubtime:
        pubtime = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        pubtime=pubtime
    return pubtime




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

date_time = time.localtime()
for line in sys.stdin:
    try:
        line = json.loads(line)
        line = line['response_body']
        # result = []
        # result.append(''.join(re.findall(u'商铺编号：(.*?)<', line)))
        # result.append(''.join(re.findall('<title>(.*?)</title>', line)))
        # result.append(''.join(re.findall(u'"month"><em>(.*?)</em>元/月</span>', line)))
        # result.append(''.join(re.findall(u'区</i>县：</span>(.*?)</p>', line)))
        # result.append(''.join(re.findall(u'商</i>圈：</span>(.*?)</p>', line)))
        # result.append(''.join(re.findall(u'街</i>道：</span>(.*?)</p>', line)))
        # result.append(''.join(re.findall('fr time">(.*?)</span></p', line)))
        # result.append(time.strftime("%Y-%m-%d",time.localtime()))
        # result.append(time.strftime("%Y-%m-%d", time.localtime()))

        dict = {}
        dict['shopId']=''.join(re.findall(u'商铺编号：(.*?)<', line))
        dict['title'] =''.join(re.findall('<title>(.*?)</title>', line))
        dict['rent'] =''.join(re.findall(u'"month"><em>(.*?)</em>元/月</span>', line))
        dict['region'] =''.join(re.findall(u'区</i>县：</span>(.*?)</p>', line))
        dict['commercial_district'] =''.join(re.findall(u'商</i>圈：</span>(.*?)</p>', line))
        dict['street'] =''.join(re.findall(u'街</i>道：</span>(.*?)</p>', line))
        dict['update_time'] =''.join(re.findall('fr time">(.*?)</span></p', line))
        dict['tasktime'] =time.strftime("%Y-%m-%d %H:%M:%S",date_time)
        # dict[''] =time.strftime("%Y-%m-%d", time.localtime())
        dict['update_time'] = tranform_pubtime(dict['update_time'])
        print json.dumps(dict)
    except Exception,e:
        pass




# create table if NOT EXISTS tmp_test.lepu_rentalshops(`shop_id` string comment '商店编号',`title` string comment '标题', `rent` string comment '租金',  `region` string comment '区县', `commercial_district` string comment '商圈',`street` string comment '街道', `update_time` string comment '更新时间',`tasktime` string comment '任务开始时间') COMMENT 'lepu商铺信息抓取' PARTITIONED BY (`dt` date COMMENT '时间') row format delimited fields terminated by '\001';
    
    