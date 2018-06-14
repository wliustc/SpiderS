# coding=utf8
import sys
import web
import json
import datetime
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')
#db = MySQLdb.connect("localhost", "root", "110707", "shengyicanmou", charset='utf8')
db = MySQLdb.connect("10.15.1.24", "writer", "hh$writer", "hillinsight", charset='utf8')
cursor = db.cursor()
# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
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


def commit_to_mysql(sql, parm):
    try:
        # print sql
        print(parm)
        cursor.execute(sql, parm)
        db.commit()
        # db.query(sql, parm)
    except Exception as e:
        print e


def time_transform(str):
    import time
    timeArray = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray)) * 1000
    return timeStamp


def parse(line):
    line_json = json.loads(line)
    content = line_json.get('content')
    meta = line_json.get('meta')
    cate = meta.get('cate')
    d = meta.get('d')
    activityStatus = d.get('activityStatus')
    brand = meta.get('brand')
    # print cate, brand
    if cate == 'parse_act_detail_kpi_core_live':

        result = {}

        result['updateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        result['brand'] = brand
        preheatEnd = d.get('preheatEnd')
        activityEnd = d.get('activityEnd')
        # 预热期
        preheatCartByrCnt = content.get('preheatCartByrCnt')
        cltRate = content.get('cltRate')
        preheatCltItmCnt = content.get('preheatCltItmCnt')
        preheatUv = content.get('preheatUv')
        preheatCltByrCnt = content.get('preheatCltByrCnt')
        preheatCartItmCnt = content.get('preheatCartItmCnt')
        cartRate = content.get('cartRate')
        preheat_time = meta.get('preheat_time')
        if preheat_time:
            result['preheat_time'] = preheat_time
            preheatCartByrCnt = preheatCartByrCnt.get('value')
            result['preheatCartByrCnt'] = preheatCartByrCnt
            cltRate = cltRate.get('value')
            result['cltRate'] = cltRate
            preheatUv = preheatUv.get('value')
            result['preheatUv'] = preheatUv
            preheatCltByrCnt = preheatCltByrCnt.get('value')
            result['preheatCltByrCnt'] = preheatCltByrCnt
            preheatCltItmCnt = preheatCltItmCnt.get('value')
            result['preheatCltItmCnt'] = preheatCltItmCnt
            preheatCartItmCnt = preheatCartItmCnt.get('value')
            result['preheatCartItmCnt'] = preheatCartItmCnt
            cartRate = cartRate.get('value')
            result['cartRate'] = cartRate

            activityId = d.get('id')
            activityStart = d.get('activityStart')
            activityStart = time_transform(activityStart)

            activityMode = d.get('activityMode')
            actStatus = d.get('activityStatus')
            preheatEnd = d.get('preheatEnd')
            if preheatEnd:
                preheatEnd = time_transform(preheatEnd)
                result['preheatEnd'] = preheatEnd
            else:
                preheatEnd = ''
                result['preheatEnd'] = preheatEnd
            platformActivityId = d.get('platformActivityId')
            activityType = d.get('activityType')
            preheatStart = d.get('preheatStart')
            if preheatStart:
                preheatStart = time_transform(preheatStart)
                result['preheatStart'] = preheatStart
            actName = d.get('activityName')
            activityEnd = d.get('activityEnd')
            activityEnd = time_transform(activityEnd)
            result['activityId'] = activityId
            result['activityStart'] = activityStart
            result['activityMode'] = activityMode
            result['actStatus'] = actStatus
            result['platformActivityId'] = platformActivityId
            result['activityType'] = activityType

            result['actName'] = actName.decode('utf-8')
            result['activityEnd'] = activityEnd
            # t_spider_belle_realtime_board_pre_activity_history
            sql = "replace into t_spider_belle_realtime_board_pre_activity_history (updateTime, brand,preheat_time, preheatCartByrCnt," \
                  "cltRate,preheatUv,preheatCltByrCnt,preheatCltItmCnt,preheatCartItmCnt,cartRate,preheatEnd,preheatStart,activityId,activityStart,activityMode,actStatus,platformActivityId,activityType,actName,activityEnd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            # print sql
            parm = (
                result.get('updateTime'), result.get('brand'), result.get('preheat_time'),
                result.get('preheatCartByrCnt'),
                result.get('cltRate'), result.get('preheatUv'), result.get('preheatCltByrCnt'),
                result.get('preheatCltItmCnt'), result.get('preheatCartItmCnt'),
                result.get('cartRate'), result.get('preheatEnd'), result.get('preheatStart'), result.get('activityId'),
                result.get('activityStart'), result.get('activityMode'), result.get('actStatus'),
                result.get('platformActivityId'), result.get('activityType'), result.get('actName'),
                result.get('activityEnd'))
            commit_to_mysql(sql, parm)
        # 活动中
        actItmPayAmt = content.get('actItmPayAmt')
        actItmPayByrCnt = content.get('actItmPayByrCnt')
        actItmPayCnt = content.get('actItmPayCnt')
        actItmUv = content.get('actItmUv')
        payAmt = content.get('payAmt')
        payByrCnt = content.get('payByrCnt')
        payCnt = content.get('payCnt')
        payPct = content.get('payPct')
        payRate = content.get('payRate')
        uv = content.get('uv')

        activity_time = meta.get('activity_time')
        if activity_time:
            result['activity_time'] = activity_time
            actItmPayAmt = actItmPayAmt.get('value')
            result['actItmPayAmt'] = actItmPayAmt
            actItmPayByrCnt = actItmPayByrCnt.get('value')
            result['actItmPayByrCnt'] = actItmPayByrCnt
            actItmPayCnt = actItmPayCnt.get('value')
            result['actItmPayCnt'] = actItmPayCnt
            actItmUv = actItmUv.get('value')
            result['actItmUv'] = actItmUv
            payAmt = payAmt.get('value')
            result['payAmt'] = payAmt
            payByrCnt = payByrCnt.get('value')
            result['payByrCnt'] = payByrCnt
            payCnt = payCnt.get('value')
            result['payCnt'] = payCnt
            payPct = payPct.get('value')
            result['payPct'] = payPct
            payRate = payRate.get('value')
            result['payRate'] = payRate
            uv = uv.get('value')
            result['uv'] = uv
            activityId = d.get('id')
            activityStart = d.get('activityStart')
            activityStart = time_transform(activityStart)
            activityMode = d.get('activityMode')
            actStatus = d.get('activityStatus')
            preheatEnd = d.get('preheatEnd')
            if preheatEnd:
                preheatEnd = time_transform(preheatEnd)
                result['preheatEnd'] = preheatEnd
            else:
                preheatEnd = ''
                result['preheatEnd'] = preheatEnd
            platformActivityId = d.get('platformActivityId')
            activityType = d.get('activityType')
            preheatStart = d.get('preheatStart')
            if preheatStart:
                preheatStart = time_transform(preheatStart)
                result['preheatStart'] = preheatStart
            actName = d.get('activityName')
            activityEnd = d.get('activityEnd')
            activityEnd = time_transform(activityEnd)
            result['activityId'] = activityId
            result['activityStart'] = activityStart
            result['activityMode'] = activityMode
            result['actStatus'] = actStatus
            result['platformActivityId'] = platformActivityId
            result['activityType'] = activityType
            result['actName'] = actName
            result['activityEnd'] = activityEnd
            sql = "replace into t_spider_belle_realtime_board_history_activity (updateTime, brand,activity_time, actItmPayAmt," \
                  "actItmPayByrCnt,actItmPayCnt,actItmUv,payAmt,payByrCnt,payCnt,payPct,payRate,uv,preheatEnd,preheatStart,activityId,activityStart,activityMode,actStatus,platformActivityId,activityType,actName,activityEnd) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            parm = (result.get('updateTime'), result.get('brand'), result.get('activity_time'),
                    result.get('actItmPayAmt'), result.get('actItmPayByrCnt'), result.get('actItmPayCnt'),
                    result.get('actItmUv'), result.get('payAmt'), result.get('payByrCnt'),
                    result.get('payCnt'), result.get('payPct'), result.get('payRate'), result.get('uv'),
                    result.get('preheatEnd'), result.get('preheatStart'), result.get('activityId'),
                    result.get('activityStart'), result.get('activityMode'), result.get('actStatus'),
                    result.get('platformActivityId'), result.get('activityType'), result.get('actName'),
                    result.get('activityEnd'))
            commit_to_mysql(sql, parm)
    elif cate == 'parse_act_detail_hour_live':
        activity_time = meta.get('activity_time')
        actStatus = d.get('activityStatus')
        if activityStatus != 0:
            if content:
                data = content.get('data')
                if data:
                    activityResult = data.get('activityResult')
                    hour = activityResult.get('hour')
                    statHour = activityResult.get('statHour')

                    result = {}
                    for index, h_data in enumerate(hour):
                        result['_' + str(statHour[index])] = h_data
                    if meta:
                        result['brand'] = brand
                        result['updateTime'] = content.get('updateTime')
                        result['indexcode'] = meta.get('indexcode')
                        result['cate'] = activity_hour_dict.get(meta.get('indexcode'))
                        result['activityId'] = d.get('id')
                        result['activity_time'] = activity_time
                        result['actStatus'] = actStatus
                        sql = "replace into t_spider_belle_realtime_board_activity_hour_history (brand,updateTime,indexcode,cate,activityId,activity_time,_00,_01,_02,_03,_04,_05,_06,_07,_08,_09,_10,_11,_12,_13,_14,_15,_16,_17,_18,_19,_20,_21,_22,_23,actStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        parm = (
                            result.get('brand'), result.get('updateTime'), result.get('indexcode'),result.get('cate'), result.get('activityId'),
                            result.get('activity_time'), result.get('_00'),result.get('_01'),
                            result.get('_02'), result.get('_03'), result.get('_04'),result.get('_05'), result.get('_06'),result.get('_07'),
                            result.get('_08'), result.get('_09'),result.get('_10'),result.get('_11'), result.get('_12'),
                            result.get('_13'), result.get('_14'),result.get('_15'), result.get('_16'),result.get('_17'), result.get('_18'),
                            result.get('_19'), result.get('_20'),result.get('_21'), result.get('_22'), result.get('_23'),result.get('actStatus')
                        )
                        commit_to_mysql(sql, parm)
    elif cate == 'parse_realtime_popularize':
        preheat_time = meta.get('preheat_time')
        if preheat_time:
            if content:
                for i in content:
                    result = {}
                    result['updateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    result['brand'] = brand
                    device = meta.get('device')
                    result['device'] = device
                    statDate = i.get('statDate')
                    if statDate:
                        result['statDate'] = statDate.get('value')
                    else:
                        result['statDate'] = ''
                    uv = i.get('uv')
                    if uv:
                        result['uv'] = uv.get('value')
                    else:
                        result['uv'] = ''
                    cartRate = i.get('cartRate')
                    if cartRate:
                        result['cartRate'] = cartRate.get('value')
                    else:
                        result['cartRate'] = ''
                    payByrCnt = i.get('payByrCnt')
                    if payByrCnt:
                        result['payByrCnt'] = payByrCnt.get('value')
                    else:
                        result['payByrCnt'] = ''
                    payRate = i.get('payRate')
                    if payRate:
                        result['payRate'] = payRate.get('value')
                    else:
                        result['payRate'] = ''
                    payAmt = i.get('payAmt')
                    if payAmt:
                        result['payAmt'] = payAmt.get('value')
                    else:
                        result['payAmt'] = ''
                    preheatCartByrCnt = i.get('preheatCartByrCnt')
                    if preheatCartByrCnt:
                        result['preheatCartByrCnt'] = preheatCartByrCnt.get('value')
                    else:
                        result['preheatCartByrCnt'] = ''
                    preheatUv = i.get('preheatUv')
                    if preheatUv:
                        result['preheatUv'] = preheatUv.get('value')
                    else:
                        result['preheatUv'] = ''
                    cltRate = i.get('cltRate')
                    if cltRate:
                        result['cltRate'] = cltRate.get('value')
                    else:
                        result['cltRate'] = ''
                    preheatCltByrCnt = i.get('preheatCltByrCnt')
                    if preheatCltByrCnt:
                        result['preheatCltByrCnt'] = preheatCltByrCnt.get('value')
                    else:
                        result['cltRate'] = ''
                    pPageName = i.get('pPageName')
                    if pPageName:
                        result['pPageName'] = pPageName.get('value')
                    else:
                        result['pPageName'] = ''
                    pageId = i.get('pageId')
                    if pageId:
                        result['pageId'] = pageId.get('value')
                    else:
                        result['pageId'] = ''
                    pageName = i.get('pageName')
                    if pageName:
                        result['pageName'] = pageName.get('value')
                    else:
                        result['pageName'] = ''
                    pPageId = i.get('pPageId')
                    if pPageId:
                        result['pPageId'] = pPageId.get('value')
                    else:
                        result['pPageId'] = ''
                    activityId = d.get('id')
                    activityStart = d.get('activityStart')
                    activityStart = time_transform(activityStart)

                    activityMode = d.get('activityMode')
                    actStatus = d.get('activityStatus')
                    preheatEnd = d.get('preheatEnd')
                    if preheatEnd:
                        preheatEnd = time_transform(preheatEnd)
                        result['preheatEnd'] = preheatEnd
                    else:
                        preheatEnd = ''
                        result['preheatEnd'] = preheatEnd
                    platformActivityId = d.get('platformActivityId')
                    activityType = d.get('activityType')
                    preheatStart = d.get('preheatStart')
                    if preheatStart:
                        preheatStart = time_transform(preheatStart)
                        result['preheatStart'] = preheatStart
                    else:
                        preheatStart = ''
                        result['preheatStart'] = preheatStart
                    actName = d.get('activityName')
                    activityEnd = d.get('activityEnd')
                    activityEnd = time_transform(activityEnd)
                    result['activityId'] = activityId
                    result['activityStart'] = activityStart
                    result['activityMode'] = activityMode
                    result['actStatus'] = actStatus
                    result['platformActivityId'] = platformActivityId
                    result['activityType'] = activityType
                    result['activity_time'] = preheat_time
                    result['actName'] = actName.decode('utf-8')
                    result['activityEnd'] = activityEnd

                    sql = "replace into t_spider_belle_realtime_board_pre_activity_popularize_history (activityId, activityStart,activityMode, actStatus," \
                          "preheatEnd,platformActivityId,activityType,preheatStart, actName, activityEnd, brand, device,updateTime,statDate," \
                          "uv,pPageName,pageId,pageName,pPageId,cartRate,payByrCnt,payRate,payAmt,preheatCartByrCnt,preheatUv,cltRate,preheatCltByrCnt,activity_time) " \
                          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    # print sql
                    parm = (result.get('activityId'), result.get('activityStart'), result.get('activityMode'),
                            result.get('actStatus'), result.get('preheatEnd'),
                            result.get('platformActivityId'), result.get('activityType'), result.get('preheatStart'),
                            result.get('actName'), result.get('activityEnd'),
                            result.get('brand'), result.get('device'), result.get('updateTime'), result.get('statDate'),
                            result.get('uv'),
                            result.get('pPageName'), result.get('pageId'), result.get('pageName'),
                            result.get('pPageId'), result.get('cartRate'),
                            result.get('payByrCnt'), result.get('payRate'), result.get('payAmt'),
                            result.get('preheatCartByrCnt'), result.get('preheatUv'),
                            result.get('cltRate'), result.get('preheatCltByrCnt'), result.get('activity_time')
                            )
                    commit_to_mysql(sql, parm)
                    children = i.get('children')
                    for x in children:
                        result = {}
                        result['updateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        result['brand'] = brand
                        device = meta.get('device')
                        result['device'] = device
                        statDate = x.get('statDate')
                        if statDate:
                            result['statDate'] = statDate.get('value')
                        else:
                            result['statDate'] = ''
                        uv = x.get('uv')
                        if uv:
                            result['uv'] = uv.get('value')
                        else:
                            result['uv'] = ''
                        cartRate = x.get('cartRate')
                        if cartRate:
                            result['cartRate'] = cartRate.get('value')
                        else:
                            result['cartRate'] = ''
                        payByrCnt = x.get('payByrCnt')
                        if payByrCnt:
                            result['payByrCnt'] = payByrCnt.get('value')
                        else:
                            result['payByrCnt'] = ''
                        payRate = x.get('payRate')
                        if payRate:
                            result['payRate'] = payRate.get('value')
                        else:
                            result['payRate'] = ''
                        payAmt = x.get('payAmt')
                        if payAmt:
                            result['payAmt'] = payAmt.get('value')
                        else:
                            result['payAmt'] = ''
                        preheatCartByrCnt = x.get('preheatCartByrCnt')
                        if preheatCartByrCnt:
                            result['preheatCartByrCnt'] = preheatCartByrCnt.get('value')
                        else:
                            result['preheatCartByrCnt'] = ''
                        preheatUv = x.get('preheatUv')
                        if preheatUv:
                            result['preheatUv'] = preheatUv.get('value')
                        else:
                            result['preheatUv'] = ''
                        cltRate = x.get('cltRate')
                        if cltRate:
                            result['cltRate'] = cltRate.get('value')
                        else:
                            result['cltRate'] = ''
                        preheatCltByrCnt = x.get('preheatCltByrCnt')
                        if preheatCltByrCnt:
                            result['preheatCltByrCnt'] = preheatCltByrCnt.get('value')
                        else:
                            result['cltRate'] = ''
                        pPageName = x.get('pPageName')
                        if pPageName:
                            result['pPageName'] = pPageName.get('value')
                        else:
                            result['pPageName'] = ''
                        pageId = x.get('pageId')
                        if pageId:
                            result['pageId'] = pageId.get('value')
                        else:
                            result['pageId'] = ''
                        pageName = x.get('pageName')
                        if pageName:
                            result['pageName'] = pageName.get('value')
                        else:
                            result['pageName'] = ''
                        pPageId = x.get('pPageId')
                        if pPageId:
                            result['pPageId'] = pPageId.get('value')
                        else:
                            result['pPageId'] = ''
                        activityId = d.get('id')
                        activityStart = d.get('activityStart')
                        activityStart = time_transform(activityStart)

                        activityMode = d.get('activityMode')
                        actStatus = d.get('activityStatus')
                        preheatEnd = d.get('preheatEnd')
                        if preheatEnd:
                            preheatEnd = time_transform(preheatEnd)
                            result['preheatEnd'] = preheatEnd
                        else:
                            preheatEnd = ''
                            result['preheatEnd'] = preheatEnd
                        platformActivityId = d.get('platformActivityId')
                        activityType = d.get('activityType')
                        preheatStart = d.get('preheatStart')
                        if preheatStart:
                            preheatStart = time_transform(preheatStart)
                            result['preheatStart'] = preheatStart
                        else:
                            preheatStart = ''
                            result['preheatStart'] = preheatStart
                        actName = d.get('activityName')
                        activityEnd = d.get('activityEnd')
                        activityEnd = time_transform(activityEnd)
                        result['activityId'] = activityId
                        result['activityStart'] = activityStart
                        result['activityMode'] = activityMode
                        result['actStatus'] = actStatus
                        result['platformActivityId'] = platformActivityId
                        result['activityType'] = activityType
                        result['activity_time'] = preheat_time

                        result['actName'] = actName.decode('utf-8')
                        result['activityEnd'] = activityEnd
                        sql = "replace into t_spider_belle_realtime_board_pre_activity_popularize_history (activityId, activityStart,activityMode, actStatus," \
                              "preheatEnd,platformActivityId,activityType,preheatStart, actName, activityEnd, brand, device,updateTime,statDate," \
                              "uv,pPageName,pageId,pageName,pPageId,cartRate,payByrCnt,payRate,payAmt,preheatCartByrCnt,preheatUv,cltRate,preheatCltByrCnt,activity_time) " \
                              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        # print sql
                        parm = (result.get('activityId'), result.get('activityStart'), result.get('activityMode'),
                                result.get('actStatus'), result.get('preheatEnd'),
                                result.get('platformActivityId'), result.get('activityType'),
                                result.get('preheatStart'), result.get('actName'), result.get('activityEnd'),
                                result.get('brand'), result.get('device'), result.get('updateTime'),
                                result.get('statDate'), result.get('uv'),
                                result.get('pPageName'), result.get('pageId'), result.get('pageName'),
                                result.get('pPageId'), result.get('cartRate'),
                                result.get('payByrCnt'), result.get('payRate'), result.get('payAmt'),
                                result.get('preheatCartByrCnt'), result.get('preheatUv'),
                                result.get('cltRate'), result.get('preheatCltByrCnt'), result.get('activity_time')
                                )
                        commit_to_mysql(sql, parm)
        activity_time = meta.get('activity_time')
        if activity_time:
            if content:
                for i in content:
                    result = {}
                    result['updateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    result['brand'] = brand
                    device = meta.get('device')
                    result['device'] = device
                    statDate = i.get('statDate')
                    if statDate:
                        result['statDate'] = statDate.get('value')
                    else:
                        result['statDate'] = ''
                    uv = i.get('uv')
                    if uv:
                        result['uv'] = uv.get('value')
                    else:
                        result['uv'] = ''
                    cartRate = i.get('cartRate')
                    if cartRate:
                        result['cartRate'] = cartRate.get('value')
                    else:
                        result['cartRate'] = ''
                    payByrCnt = i.get('payByrCnt')
                    if payByrCnt:
                        result['payByrCnt'] = payByrCnt.get('value')
                    else:
                        result['payByrCnt'] = ''
                    payRate = i.get('payRate')
                    if payRate:
                        result['payRate'] = payRate.get('value')
                    else:
                        result['payRate'] = ''
                    payAmt = i.get('payAmt')
                    if payAmt:
                        result['payAmt'] = payAmt.get('value')
                    else:
                        result['payAmt'] = ''
                    preheatCartByrCnt = i.get('preheatCartByrCnt')
                    if preheatCartByrCnt:
                        result['preheatCartByrCnt'] = preheatCartByrCnt.get('value')
                    else:
                        result['preheatCartByrCnt'] = ''
                    preheatUv = i.get('preheatUv')
                    if preheatUv:
                        result['preheatUv'] = preheatUv.get('value')
                    else:
                        result['preheatUv'] = ''
                    cltRate = i.get('cltRate')
                    if cltRate:
                        result['cltRate'] = cltRate.get('value')
                    else:
                        result['cltRate'] = ''
                    preheatCltByrCnt = i.get('preheatCltByrCnt')
                    if preheatCltByrCnt:
                        result['preheatCltByrCnt'] = preheatCltByrCnt.get('value')
                    else:
                        result['cltRate'] = ''
                    pPageName = i.get('pPageName')
                    if pPageName:
                        result['pPageName'] = pPageName.get('value')
                    else:
                        result['pPageName'] = ''
                    pageId = i.get('pageId')
                    if pageId:
                        result['pageId'] = pageId.get('value')
                    else:
                        result['pageId'] = ''
                    pageName = i.get('pageName')
                    if pageName:
                        result['pageName'] = pageName.get('value')
                    else:
                        result['pageName'] = ''
                    pPageId = i.get('pPageId')
                    if pPageId:
                        result['pPageId'] = pPageId.get('value')
                    else:
                        result['pPageId'] = ''
                    activityId = d.get('id')
                    activityStart = d.get('activityStart')
                    activityStart = time_transform(activityStart)

                    activityMode = d.get('activityMode')
                    actStatus = d.get('activityStatus')
                    preheatEnd = d.get('preheatEnd')
                    if preheatEnd:
                        preheatEnd = time_transform(preheatEnd)
                        result['preheatEnd'] = preheatEnd
                    else:
                        preheatEnd = ''
                        result['preheatEnd'] = preheatEnd
                    platformActivityId = d.get('platformActivityId')
                    activityType = d.get('activityType')
                    preheatStart = d.get('preheatStart')
                    if preheatStart:
                        preheatStart = time_transform(preheatStart)
                        result['preheatStart'] = preheatStart
                    else:
                        preheatStart = ''
                        result['preheatStart'] = preheatStart
                    actName = d.get('activityName')
                    activityEnd = d.get('activityEnd')
                    activityEnd = time_transform(activityEnd)
                    result['activityId'] = activityId
                    result['activityStart'] = activityStart
                    result['activityMode'] = activityMode
                    result['actStatus'] = actStatus
                    result['platformActivityId'] = platformActivityId
                    result['activityType'] = activityType
                    result['activity_time'] = activity_time
                    result['actName'] = actName.decode('utf-8')
                    result['activityEnd'] = activityEnd

                    sql = "replace into t_spider_belle_realtime_board_activity_popularize_history (activityId, activityStart,activityMode, actStatus," \
                          "preheatEnd,platformActivityId,activityType,preheatStart, actName, activityEnd, brand, device,updateTime,statDate," \
                          "uv,pPageName,pageId,pageName,pPageId,cartRate,payByrCnt,payRate,payAmt,preheatCartByrCnt,preheatUv,cltRate,preheatCltByrCnt,activity_time) " \
                          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    # print sql
                    parm = (result.get('activityId'), result.get('activityStart'), result.get('activityMode'),
                            result.get('actStatus'), result.get('preheatEnd'),
                            result.get('platformActivityId'), result.get('activityType'), result.get('preheatStart'),
                            result.get('actName'), result.get('activityEnd'),
                            result.get('brand'), result.get('device'), result.get('updateTime'), result.get('statDate'),
                            result.get('uv'),
                            result.get('pPageName'), result.get('pageId'), result.get('pageName'),
                            result.get('pPageId'), result.get('cartRate'),
                            result.get('payByrCnt'), result.get('payRate'), result.get('payAmt'),
                            result.get('preheatCartByrCnt'), result.get('preheatUv'),
                            result.get('cltRate'), result.get('preheatCltByrCnt'), result.get('activity_time')
                            )
                    commit_to_mysql(sql, parm)
                    children = i.get('children')
                    for x in children:
                        result = {}
                        result['updateTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        result['brand'] = brand
                        device = meta.get('device')
                        result['device'] = device
                        statDate = x.get('statDate')
                        if statDate:
                            result['statDate'] = statDate.get('value')
                        else:
                            result['statDate'] = ''
                        uv = x.get('uv')
                        if uv:
                            result['uv'] = uv.get('value')
                        else:
                            result['uv'] = ''
                        cartRate = x.get('cartRate')
                        if cartRate:
                            result['cartRate'] = cartRate.get('value')
                        else:
                            result['cartRate'] = ''
                        payByrCnt = x.get('payByrCnt')
                        if payByrCnt:
                            result['payByrCnt'] = payByrCnt.get('value')
                        else:
                            result['payByrCnt'] = ''
                        payRate = x.get('payRate')
                        if payRate:
                            result['payRate'] = payRate.get('value')
                        else:
                            result['payRate'] = ''
                        payAmt = x.get('payAmt')
                        if payAmt:
                            result['payAmt'] = payAmt.get('value')
                        else:
                            result['payAmt'] = ''
                        preheatCartByrCnt = x.get('preheatCartByrCnt')
                        if preheatCartByrCnt:
                            result['preheatCartByrCnt'] = preheatCartByrCnt.get('value')
                        else:
                            result['preheatCartByrCnt'] = ''
                        preheatUv = x.get('preheatUv')
                        if preheatUv:
                            result['preheatUv'] = preheatUv.get('value')
                        else:
                            result['preheatUv'] = ''
                        cltRate = x.get('cltRate')
                        if cltRate:
                            result['cltRate'] = cltRate.get('value')
                        else:
                            result['cltRate'] = ''
                        preheatCltByrCnt = x.get('preheatCltByrCnt')
                        if preheatCltByrCnt:
                            result['preheatCltByrCnt'] = preheatCltByrCnt.get('value')
                        else:
                            result['cltRate'] = ''
                        pPageName = x.get('pPageName')
                        if pPageName:
                            result['pPageName'] = pPageName.get('value')
                        else:
                            result['pPageName'] = ''
                        pageId = x.get('pageId')
                        if pageId:
                            result['pageId'] = pageId.get('value')
                        else:
                            result['pageId'] = ''
                        pageName = x.get('pageName')
                        if pageName:
                            result['pageName'] = pageName.get('value')
                        else:
                            result['pageName'] = ''
                        pPageId = x.get('pPageId')
                        if pPageId:
                            result['pPageId'] = pPageId.get('value')
                        else:
                            result['pPageId'] = ''
                        activityId = d.get('id')
                        activityStart = d.get('activityStart')
                        activityStart = time_transform(activityStart)

                        activityMode = d.get('activityMode')
                        actStatus = d.get('activityStatus')
                        preheatEnd = d.get('preheatEnd')
                        if preheatEnd:
                            preheatEnd = time_transform(preheatEnd)
                            result['preheatEnd'] = preheatEnd
                        else:
                            preheatEnd = ''
                            result['preheatEnd'] = preheatEnd
                        platformActivityId = d.get('platformActivityId')
                        activityType = d.get('activityType')
                        preheatStart = d.get('preheatStart')
                        if preheatStart:
                            preheatStart = time_transform(preheatStart)
                            result['preheatStart'] = preheatStart
                        else:
                            preheatStart = ''
                            result['preheatStart'] = preheatStart
                        actName = d.get('activityName')
                        activityEnd = d.get('activityEnd')
                        activityEnd = time_transform(activityEnd)
                        result['activityId'] = activityId
                        result['activityStart'] = activityStart
                        result['activityMode'] = activityMode
                        result['actStatus'] = actStatus
                        result['platformActivityId'] = platformActivityId
                        result['activityType'] = activityType
                        result['activity_time'] = activity_time

                        result['actName'] = actName.decode('utf-8')
                        result['activityEnd'] = activityEnd
                        sql = "replace into t_spider_belle_realtime_board_activity_popularize_history (activityId, activityStart,activityMode, actStatus," \
                              "preheatEnd,platformActivityId,activityType,preheatStart, actName, activityEnd, brand, device,updateTime,statDate," \
                              "uv,pPageName,pageId,pageName,pPageId,cartRate,payByrCnt,payRate,payAmt,preheatCartByrCnt,preheatUv,cltRate,preheatCltByrCnt,activity_time) " \
                              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        # print sql
                        parm = (result.get('activityId'), result.get('activityStart'), result.get('activityMode'),
                                result.get('actStatus'), result.get('preheatEnd'),
                                result.get('platformActivityId'), result.get('activityType'),
                                result.get('preheatStart'), result.get('actName'), result.get('activityEnd'),
                                result.get('brand'), result.get('device'), result.get('updateTime'),
                                result.get('statDate'), result.get('uv'),
                                result.get('pPageName'), result.get('pageId'), result.get('pageName'),
                                result.get('pPageId'), result.get('cartRate'),
                                result.get('payByrCnt'), result.get('payRate'), result.get('payAmt'),
                                result.get('preheatCartByrCnt'), result.get('preheatUv'),
                                result.get('cltRate'), result.get('preheatCltByrCnt'), result.get('activity_time')
                                )
                        commit_to_mysql(sql, parm)


for line in sys.stdin:
    parse(line)
# db1 = web.database(dbn='mysql', db='shengyicanmou', user='root', pw='110707', port=3306, host='127.0.0.1')
db1 = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
sql1 = 'select updateTime,actItmPayCnt,payPct,activityType,actName ,actItmPayByrCnt ,platformActivityId ,activityId ,payRate ,actStatus ,actItmPayAmt ,payAmt ,brand ,activityStart ,preheatEnd ,activityMode ,uv ,actItmUv ,preheatStart ,ORDER_BY_TIME ,payCnt ,activityEnd ,payByrCnt ,preheatCartByrCnt ,cltRate ,preheatUv ,preheatCltByrCnt ,preheatCltItmCnt ,preheatCartItmCnt ,statDate ,cartRate ,preheat_time from  t_spider_belle_realtime_board_pre_activity_history where actStatus != "3";'

data = db1.query(sql1)
for i in data:
    sql = 'insert into t_spider_belle_realtime_board_pre_activity(updateTime,actItmPayCnt,payPct,activityType,actName ,actItmPayByrCnt ,platformActivityId ,' \
          'activityId ,payRate ,actStatus ,actItmPayAmt ,payAmt ,brand ,activityStart ,preheatEnd ,activityMode ,uv ,actItmUv ,preheatStart ,ORDER_BY_TIME ,payCnt ,activityEnd ,payByrCnt ,' \
          'preheatCartByrCnt ,cltRate ,preheatUv ,preheatCltByrCnt ,preheatCltItmCnt ,preheatCartItmCnt ,statDate ,cartRate ,preheat_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    i['updateTime'] = i['preheat_time'] + " 23:59:59"
    parm = (i.get('updateTime'), i.get('actItmPayCnt'), i.get('payPct'), i.get('activityType'), i.get('actName'),
            i.get('actItmPayByrCnt'), i.get('platformActivityId'), i.get('activityId'), i.get('payRate'),
            i.get('actStatus'),
            i.get('actItmPayAmt'), i.get('payAmt'), i.get('brand'), i.get('activityStart'), i.get('preheatEnd'),
            i.get('activityMode'),
            i.get('uv'), i.get('actItmUv'), i.get('preheatStart'), i.get('ORDER_BY_TIME'), i.get('payCnt'),
            i.get('activityEnd'), i.get('payByrCnt'),
            i.get('preheatCartByrCnt'), i.get('cltRate'), i.get('preheatUv'), i.get('preheatCltByrCnt'),
            i.get('preheatCltItmCnt'), i.get('preheatCartItmCnt'), i.get('statDate'), i.get('cartRate'),
            i.get('preheat_time'))
    commit_to_mysql(sql, parm)

sql2 = 'select updateTime,actItmPayCnt,payPct,activityType,actName,actItmPayByrCnt,platformActivityId,activityId,payRate,actStatus,actItmPayAmt,payAmt,brand,activityStart,preheatEnd,activityMode,uv,actItmUv,preheatStart,ORDER_BY_TIME,payCnt,activityEnd,payByrCnt,activity_time from  t_spider_belle_realtime_board_history_activity where actStatus != "3";'

data = db1.query(sql2)
for i in data:
    sql = 'insert into t_spider_belle_realtime_board_activity(updateTime,actItmPayCnt,payPct,activityType,actName,actItmPayByrCnt,' \
          'platformActivityId,activityId,payRate,actStatus,actItmPayAmt,payAmt,brand,activityStart,preheatEnd,activityMode,uv,actItmUv,' \
          'preheatStart,ORDER_BY_TIME,payCnt,activityEnd,payByrCnt,activity_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    i['updateTime'] = i['activity_time'] + " 23:59:59"
    parm = (i.get('updateTime'), i.get('actItmPayCnt'), i.get('payPct'), i.get('activityType'), i.get('actName'),
            i.get('actItmPayByrCnt'), i.get('platformActivityId'), i.get('activityId'), i.get('payRate'),
            i.get('actStatus'),
            i.get('actItmPayAmt'), i.get('payAmt'), i.get('brand'), i.get('activityStart'), i.get('preheatEnd'),
            i.get('activityMode'), i.get('uv'), i.get('actItmUv'), i.get('preheatStart'), i.get('ORDER_BY_TIME'),
            i.get('payCnt'), i.get('activityEnd'), i.get('payByrCnt'), i.get('activity_time'))
    print(parm)
    commit_to_mysql(sql, parm)

sql3 = 'select * from t_spider_belle_realtime_board_activity_hour_history where actStatus != "3";'
data = db1.query(sql3)
for i in data:
    sql = "replace into t_spider_belle_realtime_board_activity_hour (brand,updateTime,indexcode,cate,activityId,activity_time,_00,_01,_02,_03,_04,_05,_06,_07,_08,_09,_10,_11,_12,_13,_14,_15,_16,_17,_18,_19,_20,_21,_22,_23,actStatus) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    i['updateTime'] = i['activity_time'] + " 23:59:59"
    parm = (
        i.get('brand'), i.get('updateTime'), i.get('indexcode'),i.get('cate'), i.get('activityId'),
        i.get('activity_time'), i.get('_00'),i.get('_01'),i.get('_02'), i.get('_03'), i.get('_04'),
        i.get('_05'), i.get('_06'),i.get('_07'),i.get('_08'), i.get('_09'),i.get('_10'),i.get('_11'),
        i.get('_12'),i.get('_13'), i.get('_14'),i.get('_15'), i.get('_16'),i.get('_17'), i.get('_18'),
        i.get('_19'), i.get('_20'),i.get('_21'), i.get('_22'), i.get('_23'),i.get('actStatus')
    )

    commit_to_mysql(sql, parm)

sql4 = 'select * from t_spider_belle_realtime_board_pre_activity_popularize_history  where actStatus != "3";'
data = db1.query(sql4)
for i in data:
    sql = "replace into t_spider_belle_realtime_board_pre_activity_popularize (activityId, activityStart,activityMode, actStatus," \
          "preheatEnd,platformActivityId,activityType,preheatStart, actName, activityEnd, brand, device,updateTime,statDate," \
          "uv,pPageName,pageId,pageName,pPageId,cartRate,payByrCnt,payRate,payAmt,preheatCartByrCnt,preheatUv,cltRate,preheatCltByrCnt,activity_time) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # print sql
    i['updateTime'] = i['activity_time'] + " 23:59:59"
    parm = (i.get('activityId'), i.get('activityStart'), i.get('activityMode'),i.get('actStatus'), i.get('preheatEnd'),
            i.get('platformActivityId'), i.get('activityType'), i.get('preheatStart'),i.get('actName'), i.get('activityEnd'),
            i.get('brand'), i.get('device'), i.get('updateTime'), i.get('statDate'),i.get('uv'),
            i.get('pPageName'), i.get('pageId'), i.get('pageName'),i.get('pPageId'), i.get('cartRate'),
            i.get('payByrCnt'), i.get('payRate'), i.get('payAmt'),i.get('preheatCartByrCnt'), i.get('preheatUv'),
            i.get('cltRate'), i.get('preheatCltByrCnt'), i.get('activity_time')
            )
    commit_to_mysql(sql, parm)

sql5 = 'select * from t_spider_belle_realtime_board_activity_popularize_history where actStatus != "3";'
data = db1.query(sql5)
for i in data:
    sql = "replace into t_spider_belle_realtime_board_activity_popularize (activityId, activityStart,activityMode, actStatus," \
          "preheatEnd,platformActivityId,activityType,preheatStart, actName, activityEnd, brand, device,updateTime,statDate," \
          "uv,pPageName,pageId,pageName,pPageId,cartRate,payByrCnt,payRate,payAmt,preheatCartByrCnt,preheatUv,cltRate,preheatCltByrCnt,activity_time) " \
          "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # print sql
    i['updateTime'] = i['activity_time'] + " 23:59:59"
    parm = (i.get('activityId'), i.get('activityStart'), i.get('activityMode'),
            i.get('actStatus'), i.get('preheatEnd'),
            i.get('platformActivityId'), i.get('activityType'),
            i.get('preheatStart'), i.get('actName'), i.get('activityEnd'),
            i.get('brand'), i.get('device'), i.get('updateTime'),
            i.get('statDate'), i.get('uv'),
            i.get('pPageName'), i.get('pageId'), i.get('pageName'),
            i.get('pPageId'), i.get('cartRate'),
            i.get('payByrCnt'), i.get('payRate'), i.get('payAmt'),
            i.get('preheatCartByrCnt'), i.get('preheatUv'),
            i.get('cltRate'), i.get('preheatCltByrCnt'), i.get('activity_time')
            )
    commit_to_mysql(sql, parm)
