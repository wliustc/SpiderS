# coding=utf8

import sys
import time
import web
import json

reload(sys)
sys.setdefaultencoding('utf-8')

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
#db = web.database(dbn='mysql', db='shengyicanmou', user='root', pw='110707', port=3306, host='127.0.0.1')

flow_payamt_list = ['pvPc',
                    'payAmtWireless',
                    'itemFavCnt',
                    'addCartItemCnt',
                    'payBuyerCntPc',
                    'newUv',
                    'itemFavCntPc',
                    'itemFavCntWireless',
                    'payItemQty',
                    'itemUv',
                    'addCartBuyerCnt',
                    'favCnt',
                    'pv',
                    'uvPc',
                    'payOrderCntWireless',
                    'itemUvWireless',
                    'payBuyerCntWireless',
                    'crtOrdBuyerCnt',
                    'uvWireless',
                    'favBuyerCnt',
                    'addCartItemCntPc',
                    'payItemQtyPc',
                    'payBuyerCnt',
                    'payAmt',
                    'brand',
                    'updateTime',
                    'addCartItemCntWireless',
                    'pvWireless',
                    'uv',
                    'payOrderCntPc',
                    'itemUvPc',
                    'payAmtPc',
                    'payOrderCnt',
                    'payItemQtyWireless']
item_top_list = ['discountPrice',
                 'itemFavCnt',
                 'addCartItemCnt',
                 'buyerCnt',
                 'indexValue',
                 'payItemQty',
                 'auctionId',
                 'pv',
                 'title',
                 'pictUrl',
                 'reservePrice',
                 'startsStr',
                 'online',
                 'gmv',
                 'payAmt',
                 'itemPicUrl',
                 'mallItem',
                 'itemDetailUrl',
                 'itemId',
                 'starts',
                 'uv',
                 'payRate',
                 'quantity']
activity_hour_dict = {
    'actItmPayAmt': u'活动商品支付金额',
    'payAmt': u'支付金额',
    'payCnt': u'支付件数',
    'actItmPayCnt': u'活动商品支付件数',
    'payByrCnt': u'支付买家数',
    'actItmPayByrCnt': u'活动商品支付买家数',
    'uv': u'访客数',
    'preheatCartByrCnt': u'预热加购人数',
    'preheatCartItmCnt': u'预热加购件数',
    'preCltByrCnt': u'预热商品收藏人数',
    'preheatCltItmCnt': u'预热收藏次数',
    'preheatUv': u'预热访客数'
}


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
    d = meta.get('d')
    brand = meta.get('brand')
    print cate, brand
    if cate == 'parse_act_detail_kpi_core_live':
        result = {}
        # print content
        updateTime = content.get('updateTime')
        result['brand'] = brand
        result['updateTime'] = updateTime
        data = content.get('data')
        actStatus = d.get('actStatus')
        if str(actStatus) == '1':
            # 预热期
            preheatCartByrCnt = data.get('preheatCartByrCnt').get('value')
            cltRate = data.get('cltRate').get('value')
            preheatUv = data.get('preheatUv').get('value')
            preheatCltByrCnt = data.get('preheatCltByrCnt').get('value')
            preheatCltItmCnt = data.get('preheatCltItmCnt').get('value')
            preheatCartItmCnt = data.get('preheatCartItmCnt').get('value')
            statDate = data.get('statDate').get('value')
            cartRate = data.get('cartRate').get('value')

            result['preheatCartByrCnt'] = preheatCartByrCnt
            result['cltRate'] = cltRate
            result['preheatUv'] = preheatUv
            result['preheatCltByrCnt'] = preheatCltByrCnt
            result['preheatCltItmCnt'] = preheatCltItmCnt
            result['preheatCartItmCnt'] = preheatCartItmCnt
            result['statDate'] = statDate
            result['cartRate'] = cartRate

            activityId = d.get('activityId')
            activityStart = d.get('activityStart')
            activityMode = d.get('activityMode')
            actStatus = d.get('actStatus')
            preheatEnd = d.get('preheatEnd')
            platformActivityId = d.get('platformActivityId')
            activityType = d.get('activityType')
            preheatStart = d.get('preheatStart')
            ORDER_BY_TIME = d.get('ORDER_BY_TIME')
            actName = d.get('actName')
            activityEnd = d.get('activityEnd')
            result['activityId'] = activityId
            result['activityStart'] = activityStart
            result['activityMode'] = activityMode
            result['actStatus'] = actStatus
            result['preheatEnd'] = preheatEnd
            result['platformActivityId'] = platformActivityId
            result['activityType'] = activityType
            result['preheatStart'] = preheatStart
            result['ORDER_BY_TIME'] = ORDER_BY_TIME
            result['actName'] = actName
            result['activityEnd'] = activityEnd
            insert_data('t_spider_belle_realtime_board_pre_activity', result)
        elif str(actStatus) == '2':
            # 活动中
            actItmPayAmt = data.get('actItmPayAmt').get('value')
            actItmPayByrCnt = data.get('actItmPayByrCnt').get('value')
            actItmPayCnt = data.get('actItmPayCnt').get('value')
            actItmUv = data.get('actItmUv').get('value')
            payAmt = data.get('payAmt').get('value')
            payByrCnt = data.get('payByrCnt').get('value')
            payCnt = data.get('payCnt').get('value')
            payPct = data.get('payPct').get('value')
            payRate = data.get('payRate').get('value')
            uv = data.get('uv').get('value')
            result['actItmPayAmt'] = actItmPayAmt
            result['actItmPayByrCnt'] = actItmPayByrCnt
            result['actItmPayCnt'] = actItmPayCnt
            result['actItmUv'] = actItmUv
            result['payAmt'] = payAmt
            result['payByrCnt'] = payByrCnt
            result['payCnt'] = payCnt
            result['payPct'] = payPct
            result['payRate'] = payRate
            result['uv'] = uv
            activityId = d.get('activityId')
            activityStart = d.get('activityStart')
            activityMode = d.get('activityMode')
            actStatus = d.get('actStatus')
            preheatEnd = d.get('preheatEnd')
            platformActivityId = d.get('platformActivityId')
            activityType = d.get('activityType')
            preheatStart = d.get('preheatStart')
            ORDER_BY_TIME = d.get('ORDER_BY_TIME')
            actName = d.get('actName')
            activityEnd = d.get('activityEnd')
            result['activityId'] = activityId
            result['activityStart'] = activityStart
            result['activityMode'] = activityMode
            result['actStatus'] = actStatus
            result['preheatEnd'] = preheatEnd
            result['platformActivityId'] = platformActivityId
            result['activityType'] = activityType
            result['preheatStart'] = preheatStart
            result['ORDER_BY_TIME'] = ORDER_BY_TIME
            result['actName'] = actName
            result['activityEnd'] = activityEnd
            # result['activity_time'] = updateTime
            # print result
            # db.insert('t_spider_belle_realtime_board_activity',**result)
            insert_data('t_spider_belle_realtime_board_activity', result)
        else:
            print actStatus

    elif cate == 'parse_act_item_live':
        result = {}
        updateTime = content.get('updateTime')
        activityId = d.get('activityId')
        activityStart = d.get('activityStart')
        activityMode = d.get('activityMode')
        actStatus = d.get('actStatus')
        preheatEnd = d.get('preheatEnd')
        platformActivityId = d.get('platformActivityId')
        activityType = d.get('activityType')
        preheatStart = d.get('preheatStart')
        ORDER_BY_TIME = d.get('ORDER_BY_TIME')
        actName = d.get('actName')
        activityEnd = d.get('activityEnd')
        result['activityId'] = activityId
        result['activityStart'] = activityStart
        result['activityMode'] = activityMode
        result['actStatus'] = actStatus
        result['preheatEnd'] = preheatEnd
        result['platformActivityId'] = platformActivityId
        result['activityType'] = activityType
        result['preheatStart'] = preheatStart
        result['ORDER_BY_TIME'] = ORDER_BY_TIME
        result['actName'] = actName
        result['activityEnd'] = activityEnd
        result['brand'] = brand
        result['updateTime'] = updateTime
        data = content.get('data')
        actStatus = d.get('actStatus')
        if str(actStatus) == '1':
            # 预热期
            # print result
            data = data.get('data')
            if data:
                for d in data:
                    itemId = d.get('itemId')
                    uv = d.get('uv')
                    cltItmQty = d.get('cltItmQty')
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
                    result['itemId'] = itemId
                    result['uv'] = uv
                    result['cltItmQty'] = cltItmQty
                    result['cartCnt'] = cartCnt
                    result['cartByrCnt'] = cartByrCnt
                    result['cartConversioRate'] = cartConversioRate
                    result['cltRate'] = cltRate
                    result['isActItem'] = isActItem
                    result['cltByrCnt'] = cltByrCnt
                    result['quantity'] = quantity
                    result['pictUrl'] = pictUrl
                    result['detailUrl'] = detailUrl
                    result['title'] = title
                    result['startDate'] = startDate
                    # 预热期
                    print result
                    insert_data('t_spider_belle_realtime_board_pre_activity_item', result)

        elif str(actStatus) == '2':
            # 活动期
            # print result
            data = data.get('data')
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
                    result['itemId'] = itemId
                    result['uv'] = uv
                    result['payRate'] = payRate
                    result['isActItem'] = isActItem
                    result['payItmCnt'] = payItmCnt
                    result['itemPayAmt'] = itemPayAmt
                    result['payBuyerCnt'] = payBuyerCnt
                    result['startDate'] = startDate
                    result['title'] = title
                    result['pictUrl'] = pictUrl
                    result['detailUrl'] = detailUrl
                    result['quantity'] = quantity
                    # db.insert('t_spider_belle_realtime_board_activity_item', **result)
                    insert_data('t_spider_belle_realtime_board_activity_item', result)

    elif cate == 'parse_realtime_flow':
        result = {}
        updateTime = content.get('updateTime')
        # print updateTime
        brand = meta.get('brand')
        result['updateTime'] = updateTime
        result['brand'] = brand
        data = content.get('data')
        if data:
            for key, val in data.items():
                # print key,val
                if 'cycleCrc' in val:
                    result[key + 'Crc'] = data.get(key).get('cycleCrc')
                if 'value' in val:
                    result[key] = data.get(key).get('value')
            # print result
            insert_data('t_spider_belle_realtime_board_flow', result)

    elif cate == 'parse_realtime_overview_flow_payamt':
        if content:
            data = content.get('data')
            if data:
                result = {}
                for key, val in data.items():
                    if key in flow_payamt_list:
                        result[key] = val
                if meta:
                    flow_content = meta.get('flow_content')
                    if flow_content:
                        flow_data = flow_content.get('data')
                        if flow_data:
                            for key, val in flow_data.items():
                                if key in flow_payamt_list:
                                    result[key] = val
                            result['brand'] = brand
                            result['updateTime'] = content.get('updateTime')
                            insert_data('t_spider_belle_realtime_board_overview_flow_payamt', result)

    elif cate == 'parse_realtime_item_top':
        if content:
            data = content.get('data')
            # print data
            if data:
                data_list = data.get('list')
                if data_list:
                    for dl in data_list:
                        result = {}
                        for key, val in dl.items():
                            if key == 'itemModel':
                                dl_itm = dl.get('itemModel')
                                if dl_itm:
                                    for ki, vi in dl_itm.items():
                                        if ki in item_top_list:
                                            result[ki] = vi
                            else:
                                if key in item_top_list:
                                    result[key] = val
                        result['brand'] = brand
                        result['updateTime'] = content.get('updateTime')
                        insert_data('t_spider_belle_realtime_board_item_top', result)

    elif cate == 'parse_act_detail_hour_live':
        if content:
            data = content.get('data')
            if data:
                activityResult = data.get('activityResult')
                hour = activityResult.get('hour')
                statHour = activityResult.get('statHour')

                result = {}
                for index, h_data in enumerate(hour):
                    result['_' + str(statHour[index])] = h_data
                # print meta
                if meta:
                    result['brand'] = brand
                    result['updateTime'] = content.get('updateTime')
                    result['indexcode'] = meta.get('indexcode')
                    result['cate'] = activity_hour_dict.get(meta.get('indexcode'))
                    result['activityId'] = d.get('activityId')
                    # print result
                    insert_data('t_spider_belle_realtime_board_activity_hour', result)
    elif cate == 'parse_realtime_popularize':
        if content:
            actStatus = d.get('actStatus')
            if str(actStatus) == '1':
                updateTime = content.get('updateTime')
                data = content.get('data')
                if data:
                    for i in data:
                        result = {}
                        result['brand'] = brand
                        device = meta.get('device')
                        result['device'] = device
                        result['updateTime'] = updateTime
                        statDate = i.get('statDate')
                        if statDate:
                            result['statDate'] = statDate.get('value')
                        uv = i.get('uv')
                        if uv:
                            result['uv'] = uv.get('value')
                        pPageName = i.get('pPageName')
                        if pPageName:
                            result['pPageName'] = pPageName.get('value')
                        pageId = i.get('pageId')
                        if pageId:
                            result['pageId'] = pageId.get('value')
                        pageName = i.get('pageName')
                        if pageName:
                            result['pageName'] = pageName.get('value')
                        pPageId = i.get('pPageId')
                        if pPageId:
                            result['pPageId'] = pPageId.get('value')

                        activityId = d.get('activityId')
                        activityStart = d.get('activityStart')
                        activityMode = d.get('activityMode')
                        actStatus = d.get('actStatus')
                        preheatEnd = d.get('preheatEnd')
                        platformActivityId = d.get('platformActivityId')
                        activityType = d.get('activityType')
                        preheatStart = d.get('preheatStart')
                        ORDER_BY_TIME = d.get('ORDER_BY_TIME')
                        actName = d.get('actName')
                        activityEnd = d.get('activityEnd')
                        result['activityId'] = activityId
                        result['activityStart'] = activityStart
                        result['activityMode'] = activityMode
                        result['actStatus'] = actStatus
                        result['preheatEnd'] = preheatEnd
                        result['platformActivityId'] = platformActivityId
                        result['activityType'] = activityType
                        result['preheatStart'] = preheatStart
                        result['ORDER_BY_TIME'] = ORDER_BY_TIME
                        result['actName'] = actName
                        result['activityEnd'] = activityEnd
                        insert_data('t_spider_belle_realtime_board_pre_activity_popularize', result)
                        children = i.get('children')
                        if children:
                            for x in children:
                                result = {}
                                result['brand'] = brand
                                device = meta.get('device')
                                result['device'] = device
                                result['updateTime'] = updateTime
                                result['statDate'] = x.get('statDate')
                                if statDate:
                                    result['statDate'] = statDate.get('value')
                                uv = x.get('uv')
                                if uv:
                                    result['uv'] = uv.get('value')
                                pPageName = x.get('pPageName')
                                if pPageName:
                                    result['pPageName'] = pPageName.get('value')
                                pageId = x.get('pageId')
                                if pageId:
                                    result['pageId'] = pageId.get('value')
                                pageName = x.get('pageName')
                                if pageName:
                                    result['pageName'] = pageName.get('value')
                                pPageId = x.get('pPageId')
                                if pPageId:
                                    result['pPageId'] = pPageId.get('value')
                                activityId = d.get('activityId')
                                activityStart = d.get('activityStart')
                                activityMode = d.get('activityMode')
                                actStatus = d.get('actStatus')
                                preheatEnd = d.get('preheatEnd')
                                platformActivityId = d.get('platformActivityId')
                                activityType = d.get('activityType')
                                preheatStart = d.get('preheatStart')
                                ORDER_BY_TIME = d.get('ORDER_BY_TIME')
                                actName = d.get('actName')
                                activityEnd = d.get('activityEnd')
                                result['activityId'] = activityId
                                result['activityStart'] = activityStart
                                result['activityMode'] = activityMode
                                result['actStatus'] = actStatus
                                result['preheatEnd'] = preheatEnd
                                result['platformActivityId'] = platformActivityId
                                result['activityType'] = activityType
                                result['preheatStart'] = preheatStart
                                result['ORDER_BY_TIME'] = ORDER_BY_TIME
                                result['actName'] = actName
                                result['activityEnd'] = activityEnd
                                insert_data('t_spider_belle_realtime_board_pre_activity_popularize', result)
            elif str(actStatus) == '2':
                # 活动期
                updateTime = content.get('updateTime')
                data = content.get('data')
                if data:
                    for i in data:
                        result = {}
                        result['brand'] = brand
                        device = meta.get('device')
                        result['device'] = device
                        result['updateTime'] = updateTime
                        statDate = i.get('statDate')
                        if statDate:
                            result['statDate'] = statDate.get('value')
                        uv = i.get('uv')
                        if uv:
                            result['uv'] = uv.get('value')
                        pPageName = i.get('pPageName')
                        if pPageName:
                            result['pPageName'] = pPageName.get('value')
                        pageId = i.get('pageId')
                        if pageId:
                            result['pageId'] = pageId.get('value')
                        pageName = i.get('pageName')
                        if pageName:
                            result['pageName'] = pageName.get('value')
                        pPageId = i.get('pPageId')
                        if pPageId:
                            result['pPageId'] = pPageId.get('value')

                        activityId = d.get('activityId')
                        activityStart = d.get('activityStart')
                        activityMode = d.get('activityMode')
                        actStatus = d.get('actStatus')
                        preheatEnd = d.get('preheatEnd')
                        platformActivityId = d.get('platformActivityId')
                        activityType = d.get('activityType')
                        preheatStart = d.get('preheatStart')
                        ORDER_BY_TIME = d.get('ORDER_BY_TIME')
                        actName = d.get('actName')
                        activityEnd = d.get('activityEnd')
                        result['activityId'] = activityId
                        result['activityStart'] = activityStart
                        result['activityMode'] = activityMode
                        result['actStatus'] = actStatus
                        result['preheatEnd'] = preheatEnd
                        result['platformActivityId'] = platformActivityId
                        result['activityType'] = activityType
                        result['preheatStart'] = preheatStart
                        result['ORDER_BY_TIME'] = ORDER_BY_TIME
                        result['actName'] = actName
                        result['activityEnd'] = activityEnd
                        # print result
                        insert_data('t_spider_belle_realtime_board_activity_popularize', result)
                        children = i.get('children')
                        if children:
                            for x in children:
                                result = {}
                                result['brand'] = brand
                                device = meta.get('device')
                                result['device'] = device
                                result['updateTime'] = updateTime
                                result['statDate'] = x.get('statDate')
                                if statDate:
                                    result['statDate'] = statDate.get('value')
                                uv = x.get('uv')
                                if uv:
                                    result['uv'] = uv.get('value')
                                pPageName = x.get('pPageName')
                                if pPageName:
                                    result['pPageName'] = pPageName.get('value')
                                pageId = x.get('pageId')
                                if pageId:
                                    result['pageId'] = pageId.get('value')
                                pageName = x.get('pageName')
                                if pageName:
                                    result['pageName'] = pageName.get('value')
                                pPageId = x.get('pPageId')
                                if pPageId:
                                    result['pPageId'] = pPageId.get('value')
                                activityId = d.get('activityId')
                                activityStart = d.get('activityStart')
                                activityMode = d.get('activityMode')
                                actStatus = d.get('actStatus')
                                preheatEnd = d.get('preheatEnd')
                                platformActivityId = d.get('platformActivityId')
                                activityType = d.get('activityType')
                                preheatStart = d.get('preheatStart')
                                ORDER_BY_TIME = d.get('ORDER_BY_TIME')
                                actName = d.get('actName')
                                activityEnd = d.get('activityEnd')
                                result['activityId'] = activityId
                                result['activityStart'] = activityStart
                                result['activityMode'] = activityMode
                                result['actStatus'] = actStatus
                                result['preheatEnd'] = preheatEnd
                                result['platformActivityId'] = platformActivityId
                                result['activityType'] = activityType
                                result['preheatStart'] = preheatStart
                                result['ORDER_BY_TIME'] = ORDER_BY_TIME
                                result['actName'] = actName
                                result['activityEnd'] = activityEnd
                                # print result
                                insert_data('t_spider_belle_realtime_board_activity_popularize', result)
    elif cate == 'parse_data':

        result = {}
        updateTime = content.get('updateTime')
        activityId = d.get('activityId')
        activityStart = d.get('activityStart')
        activityMode = d.get('activityMode')
        actStatus = d.get('actStatus')
        preheatEnd = d.get('preheatEnd')
        platformActivityId = d.get('platformActivityId')
        activityType = d.get('activityType')
        preheatStart = d.get('preheatStart')
        ORDER_BY_TIME = d.get('ORDER_BY_TIME')
        actName = d.get('actName')
        activityEnd = d.get('activityEnd')
        result['activityId'] = activityId
        result['activityStart'] = activityStart
        result['activityMode'] = activityMode
        result['actStatus'] = actStatus
        result['preheatEnd'] = preheatEnd
        result['platformActivityId'] = platformActivityId
        result['activityType'] = activityType
        result['preheatStart'] = preheatStart
        result['ORDER_BY_TIME'] = ORDER_BY_TIME
        result['actName'] = actName
        result['activityEnd'] = activityEnd
        result['brand'] = brand
        result['updateTime'] = updateTime
        data = content.get('data')
        actStatus = d.get('actStatus')
        if str(actStatus) == '1':
            # 预热期
            # print result
            data = data.get('data')
            if data:
                for d in data:
                    itemId = d.get('itemId')
                    uv = d.get('uv')
                    cltItmQty = d.get('cltItmQty')
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
                    result['itemId'] = itemId
                    result['uv'] = uv
                    result['cltItmQty'] = cltItmQty
                    result['cartCnt'] = cartCnt
                    result['cartByrCnt'] = cartByrCnt
                    result['cartConversioRate'] = cartConversioRate
                    result['cltRate'] = cltRate
                    result['isActItem'] = isActItem
                    result['cltByrCnt'] = cltByrCnt
                    result['quantity'] = quantity
                    result['pictUrl'] = pictUrl
                    result['detailUrl'] = detailUrl
                    result['title'] = title
                    result['startDate'] = startDate
                    # 预热期
                    print result
                    insert_data('t_spider_belle_realtime_board_pre_activity_total_item_data', result)

        elif str(actStatus) == '2':
            # 活动期
            # print result
            data = data.get('data')
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
                    result['itemId'] = itemId
                    result['uv'] = uv
                    result['payRate'] = payRate
                    result['isActItem'] = isActItem
                    result['payItmCnt'] = payItmCnt
                    result['itemPayAmt'] = itemPayAmt
                    result['payBuyerCnt'] = payBuyerCnt
                    result['startDate'] = startDate
                    result['title'] = title
                    result['pictUrl'] = pictUrl
                    result['detailUrl'] = detailUrl
                    result['quantity'] = quantity
                    # db.insert('t_spider_belle_realtime_board_activity_item', **result)
                    insert_data('t_spider_belle_realtime_board_activity_total_item_data', result)


for line in sys.stdin:
    parse(line)
    