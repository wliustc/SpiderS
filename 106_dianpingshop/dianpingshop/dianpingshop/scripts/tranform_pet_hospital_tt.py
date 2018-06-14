import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
import time
import web


# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
# db = web.database(dbn='mysql', db='o2o', user='root', pw='123456', port=3306, host='127.0.0.1')
db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


def multi_insert(table,data_list):

    try:
        db.multiple_insert(table, values=data_list)
    except Exception, e:
        print e


def web_db_insert(item):
#     try:
#         db.insert('t_hh_dianping_tuangou_deal_info',**data)
#     except:
#         pass
    key_str = ','.join('`%s`' % k for k in item.keys())
    value_str = ','.join(
        'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v) for v in
        item.values())
    kv_str = ','.join(
        "`%s`=%s" % (k, 'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v))
        for (k, v)
        in item.items())
    # print kv_str
    # print key_str

    sql = "INSERT INTO t_hh_dianping_shop_info_pet_hospital_tt(%s) VALUES(%s)" % (key_str, value_str)
    sql = "%s ON DUPLICATE KEY UPDATE %s" % (sql, kv_str)
    print sql
    # with open('eeeeddddd','a') as f:
    #     f.write(sql+'\n')
    # time.sleep(100)
    db.query(sql)
    # return item


def parse1(line):
    line_json = json.loads(line)
    # print line_json
    meta = line_json.get('meta')
    response_content = line_json.get('response_content')
    # print meta
    city_id = meta.get('city_id')
    city_name = meta.get('city_name')
    district_id = meta.get('district_id')
    district_name = meta.get('district_name')
    category1_id = meta.get('category1_id')
    category1_name = meta.get('category1_name')
    category2_id = meta.get('category2_id')
    category2_name = meta.get('category2_name')
    response_content = json.loads(response_content)
    # print response_content
    shopRecordBeanList = response_content.get('shopRecordBeanList')
    if shopRecordBeanList:
        data_list = []
        for shopRecordBeanl in shopRecordBeanList:
            item = {}
            # print shopRecordBean
            shopRecordBean = shopRecordBeanl.get('shopRecordBean')
            # print shopRecordBean
            item['shop_id'] = shopRecordBean.get('shopId')
            item['shop_name'] = shopRecordBean.get('shopName')
            item['category1_id'] = category1_id
            item['category1_name'] = category1_name
            item['category2_id'] = category2_id
            item['category2_name'] = category2_name
            item['group_id'] = shopRecordBean.get('shopGroupID')
            item['group_name'] = shopRecordBean.get('shopName')
            create_dt = shopRecordBean.get('addDate')
            if create_dt:
                create_dt = create_dt.split('T')[0]
            item['create_dt'] = create_dt
            item['city_id'] = city_id
            item['city_name'] = city_name
            item['district_id'] = district_id
            item['district_name'] = district_name
            item['biz_id'] = shopRecordBean.get('bussinessAreaId')
            item['biz_name'] = shopRecordBean.get('bizRegionName')
            item['address'] = shopRecordBean.get('address')
            item['lng'] = shopRecordBean.get('geoLng')
            item['lat'] = shopRecordBean.get('geoLat')
            item['avg_price'] = shopRecordBean.get('avgPrice')
            item['shop_power'] = shopRecordBean.get('shopPower')
            item['shop_power_title'] = shopRecordBean.get('shopPowerTitle')
            item['branch_total'] = shopRecordBean.get('branchTotal')
            item['dish_tags'] = shopRecordBean.get('dishTags')
            item['display_score'] = shopRecordBean.get('displayScore')
            item['display_score1'] = shopRecordBean.get('displayScore1')
            item['display_score2'] = shopRecordBean.get('displayScore2')
            item['display_score3'] = shopRecordBean.get('displayScore3')
            item['hits'] = shopRecordBean.get('hits')
            item['month_hits'] = shopRecordBean.get('monthlyHits')
            item['phone_no'] = shopRecordBean.get('phoneNo')
            item['pic_total'] = shopRecordBean.get('picTotal')
            item['popularity'] = shopRecordBean.get('popularity')
            item['primary_tag'] = shopRecordBean.get('primaryTag')
            item['shop_tags'] = shopRecordBean.get('shopTags')
            item['shop_type'] = shopRecordBean.get('shopType')
            item['vote_total'] = shopRecordBean.get('voteTotal')
            item['wish_total'] = shopRecordBean.get('wishTotal')
            item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
            web_db_insert(item)
        #     if len(data_list)>1000:
        #         multi_insert('t_hh_dianping_shop_info',data_list)
        #         data_list = []
        #     else:
        #         data_list.append(item)
        # if len(data_list)>0:
        #     multi_insert('t_hh_dianping_shop_info', data_list)

def parse(line):
    line_json = json.loads(line)
    meta = line_json.get('meta')
    shop_response = line_json.get('shop_response')
    shop_response_json = json.loads(shop_response)
    shopInfo = shop_response_json.get('msg').get('shopInfo')
    city_id = meta.get('city_id')
    city_name = meta.get('city_name')
    district_id = meta.get('district_id')
    district_name = meta.get('district_name')
    category1_id = meta.get('category1_id')
    category1_name = meta.get('category1_name')
    category2_id = meta.get('category2_id')
    category2_name = meta.get('category2_name')
    item = {}
    item['category1_id'] = category1_id
    item['category1_name'] = category1_name
    item['category2_id'] = category2_id
    item['category2_name'] = category2_name
    item['city_id'] = city_id
    item['city_name'] = city_name
    item['district_id'] = district_id
    item['district_name'] = district_name
    hits = shopInfo.get('hits')
    if hits:
        item['hits'] = hits
    else:
        item['hits'] = 0
    monthlyHits = shopInfo.get('monthlyHits')
    if monthlyHits:
        item['month_hits'] = monthlyHits
    else:
        item['month_hits'] = 0
    item['dt'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    prevWeeklyHits = shopInfo.get('prevWeeklyHits')
    if prevWeeklyHits:
        item['prev_weekly_hits'] = prevWeeklyHits
    else:
        item['prev_weekly_hits'] = 0
    todayHits = shopInfo.get('todayHits')
    if todayHits:
        item['today_hits'] = todayHits
    else:
        item['today_hits'] = 0
    weeklyHits = shopInfo.get('weeklyHits')
    if weeklyHits:
        item['weekly_hits'] = weeklyHits
    else:
        item['weekly_hits'] = 0
    web_db_insert(item)



for line in sys.stdin:
    parse(line)
    # print line



# vote_default,

# shop_status,
