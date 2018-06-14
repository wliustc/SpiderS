# coding=utf8

import sys
import time
import web
import json

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='shengyicanmou', user='root', pw='110707', port=3306, host='127.0.0.1')

def insert_data(table, result):
    try:
        db.insert(table, **result)
    except:
        pass


def parse(line):
    line_json = json.loads(line)
    content = line_json.get('content')
    meta = line_json.get('meta')
    cate = meta.get('cate')
    activity_time = meta.get('activity_time')
    d = meta.get('d')
    brand = meta.get('brand')
    url = meta.get('url')
    print cate, brand
    result = {}
    # updateTime = content.get('updateTime')
    activityId = d.get('id')
    activityStart = d.get('activityStart')
    activityMode = d.get('activityMode')
    actStatus = d.get('activityStatus')
    preheatEnd = d.get('preheatEnd')
    platformActivityId = d.get('platformActivityId')
    activityType = d.get('activityType')
    preheatStart = d.get('preheatStart')
    # ORDER_BY_TIME = d.get('ORDER_BY_TIME')
    actName = d.get('activityName')
    activityEnd = d.get('activityEnd')
    result['activityId'] = activityId
    result['activityStart'] = activityStart
    result['activityMode'] = activityMode
    result['actStatus'] = actStatus
    result['preheatEnd'] = preheatEnd
    result['platformActivityId'] = platformActivityId
    result['activityType'] = activityType
    result['preheatStart'] = preheatStart
    # result['ORDER_BY_TIME'] = ORDER_BY_TIME
    result['actName'] = actName
    result['activityEnd'] = activityEnd
    result['brand'] = brand
    data = content.get('data')
    result['updateTime'] = activity_time

    # actStatus = d.get('actStatus')
    if 'cartCnt' in url:
        if data:
            for d in data:
                itemId = d.get('itemId')
                uv = d.get('uv')
                cltItmQty = d.get('cltItmQty')
                if cltItmQty:
                    item = d.get('item')
                    cartCnt = d.get('cartCnt')
                    cartByrCnt = d.get('cartByrCnt')
                    cartConversioRate = d.get('cartConversioRate')
                    cltRate = d.get('cltRate')
                    isActItem = d.get('isActItem')
                    cltByrCnt = d.get('cltByrCnt')
                    quantity = item.get('quantity')
                    pictUrl = item.get('pictUrl')
                    detailUrl = item.get('detailUrl')
                    title = item.get('title')
                    startDate = item.get('startDate')
                    if itemId:
                        result['itemId'] = itemId.get('value')
                    if uv:
                        result['uv'] = uv.get('value')
                        result['cltItmQty'] = cltItmQty.get('value')
                    if cartCnt:
                        result['cartCnt'] = cartCnt.get('value')
                    if cartByrCnt:
                        result['cartByrCnt'] = cartByrCnt.get('value')
                    if cartConversioRate:
                        result['cartConversioRate'] = cartConversioRate.get('value')
                    if cltRate:
                        result['cltRate'] = cltRate.get('value')
                    if isActItem:

                        result['isActItem'] = isActItem.get('value')
                    if cltByrCnt:
                        result['cltByrCnt'] = cltByrCnt.get('value')
                    result['quantity'] = quantity
                    result['pictUrl'] = pictUrl
                    result['detailUrl'] = detailUrl
                    result['title'] = title
                    result['startDate'] = startDate
                    # 预热期
                    # print result
                    # db.insert('t_spider_belle_realtime_board_pre_activity_item', **result)
                    insert_data('t_spider_belle_realtime_board_pre_activity_all_item', result)

    else:
        # 活动期
        # print result
        if data:
            for d in data:
                itemId = d.get('itemId')
                uv = d.get('uv')
                payRate = d.get('payRate')
                isActItem = d.get('isActItem')
                item = d.get('item')
                payItmCnt = d.get('payItmCnt')
                itemPayAmt = d.get('itemPayAmt')
                payBuyerCnt = d.get('payBuyerCnt')
                startDate = item.get('startDate')
                title = item.get('title')
                pictUrl = item.get('pictUrl')
                detailUrl = item.get('detailUrl')
                quantity = item.get('quantity')
                if itemId:
                    result['itemId'] = itemId.get('value')
                if uv:

                    result['uv'] = uv.get('value')
                if payRate:
                    result['payRate'] = payRate.get('value')
                if isActItem:
                    result['isActItem'] = isActItem.get('value')
                if payItmCnt:
                    result['payItmCnt'] = payItmCnt.get('value')
                if itemPayAmt:
                    result['itemPayAmt'] = itemPayAmt.get('value')
                if payBuyerCnt:
                    result['payBuyerCnt'] = payBuyerCnt.get('value')
                result['startDate'] = startDate
                result['title'] = title
                result['pictUrl'] = pictUrl
                result['detailUrl'] = detailUrl
                result['quantity'] = quantity
                # db.insert('t_spider_belle_realtime_board_activity_item', **result)
                insert_data('t_spider_belle_realtime_board_activity_all_item', result)

for line in sys.stdin:
    parse(line)

    
    
    