import sys
import json

import time

import web

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
dt = int(time.time())

def web_db_insert(data):

    db.insert('t_spider_bailingniao_order',**data)

for line in sys.stdin:
    # print line
    line_json = json.loads(line)
    # print line_json
    response_content = line_json.get('response_content')
    response_content = json.loads(response_content)
    category_id = line_json.get('category_id')
    category_name = line_json.get('category_name')
    data = response_content.get('data')
    if data:
        placeUnitInfoVoList = data.get('placeUnitInfoVoList')
        if placeUnitInfoVoList:
            for placeUnitInfo in placeUnitInfoVoList:
                placeUnitList = placeUnitInfo.get('placeUnitList')
                if placeUnitList:
                    for placeUnit in placeUnitList:
                        placeUnitSalePlanList = placeUnit.get('placeUnitSalePlanList')
                        if placeUnitSalePlanList:
                            for placeUnitSalePlan in placeUnitSalePlanList:
                                respPlaceUnitSalePlan = placeUnitSalePlan.get('respPlaceUnitSalePlan')
                                if respPlaceUnitSalePlan:
                                    placeId = respPlaceUnitSalePlan.get('placeId')
                                    if placeId:
                                        result = {}
                                        result['placeId']=placeId
                                        placeUnitId = respPlaceUnitSalePlan.get('placeUnitId')
                                        result['placeUnitId'] = placeUnitId
                                        date= respPlaceUnitSalePlan.get('date')

                                        result['date'] = date
                                        startTime= respPlaceUnitSalePlan.get('startTime')

                                        result['startTime'] = startTime
                                        endTime= respPlaceUnitSalePlan.get('endTime')

                                        result['endTime'] = endTime
                                        price= respPlaceUnitSalePlan.get('price')

                                        result['price'] = price
                                        status= respPlaceUnitSalePlan.get('status')

                                        result['status'] = status
                                        result['category_id'] = category_id
                                        result['category_name'] = category_name
                                        result['task_time'] = dt
                                        print result
                                        try:
                                            web_db_insert(result)
                                        except Exception,e:
                                            print e
                                        # print '-------'

