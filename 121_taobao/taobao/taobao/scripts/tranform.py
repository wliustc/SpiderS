# coding=utf8

import sys
import json
import web

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


def parse1(line):
    # print line
    line_json = json.loads(line)
    # print line_json
    comment_list = line_json.get('comment_list')
    title = line_json.get('title')
    price = line_json.get('price')
    sale_num = line_json.get('sale_num')
    comment_num = line_json.get('comment_num')
    comment_url = line_json.get('comment_url')
    detail_url = line_json.get('detail_url')
    for comment in comment_list:
        item = {}
        displayUserNick = comment.get('displayUserNick')
        rateContent = comment.get('rateContent')
        rateDate = comment.get('rateDate')
        item['title'] = title
        item['price'] = price.strip()
        item['sale_num'] = sale_num
        item['comment_num'] = comment_num
        item['comment_url'] = comment_url
        item['detail_url'] = detail_url
        item['displayUserNick'] = displayUserNick
        item['rateContent'] = rateContent
        item['rateDate'] = rateDate
        print item

def parse(line):
    json_line = json.loads(line)
    db.insert('t_spider_taobao_xiaoguancha',**json_line)

for line in sys.stdin:
    parse(line)

    