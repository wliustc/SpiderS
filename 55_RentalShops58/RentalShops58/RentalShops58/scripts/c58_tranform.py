# -*- encoding:utf-8 -*-
import sys

import json

import datetime
reload(sys)
sys.setdefaultencoding('utf8')


# 通过page_code和city_code获取联系人电话
def tranform_pubtime(pubtime):
    pubtime = pubtime.replace('发布：', '')
    if '天前' in pubtime:
        pubtime = int(pubtime.replace('天前', ''))
        pubtime = datetime.datetime.now() + datetime.timedelta(days=-pubtime)
        pubtime = pubtime.strftime('%Y-%m-%d')
    elif '小时前' in pubtime:
        pubtime = int(pubtime.replace('小时前', ''))
        pubtime = datetime.datetime.now() + datetime.timedelta(hours=-pubtime)
        pubtime = pubtime.strftime('%Y-%m-%d')
    elif '分钟前' in pubtime:
        pubtime = int(pubtime.replace('分钟前', ''))
        pubtime = datetime.datetime.now() + datetime.timedelta(minutes=-pubtime)
        pubtime = pubtime.strftime('%Y-%m-%d')
    elif '刚刚' in pubtime:
        pubtime = datetime.datetime.now()
        pubtime = pubtime.strftime('%Y-%m-%d')
    else:
        pubtime = '20' + pubtime.replace('.', '-')
    return pubtime


def tranform_content(content, city_name, city_code, region_file, detail_url, start_time):
    item = {}
    item['detail_url'] = detail_url
    item['city_code'] = city_code
    try:
        content_json = json.loads(content)
    except Exception, e:
        content = json.dumps(content, ensure_ascii=True)
        content_json = json.loads(content)
        if not isinstance(content_json, dict):
            content_json = json.loads(content_json)
    # print content_json
    print type(content_json)
    if 'result' in content_json:
        if 'info' in content_json['result']:
            info = content_json['result']['info']

            item['tasktime'] = start_time
            # if city_name:
            item['city'] = city_name
            for i in info:
                if 'title_area' in i:
                    item['title'] = i['title_area']['title']
                    pubtime = i['title_area']['ext'][0]
                    item['pubtime'] = tranform_pubtime(pubtime)
                    item['rent'] = i['title_area']['price']['p'] + i['title_area']['price']['u']
                if 'desc_area' in i:
                    item['describe'] = i['desc_area']['text'].replace('<br>', '')
                if 'baseinfo_area' in i:
                    if 'base_area' in i['baseinfo_area']:
                        if 'items' in i['baseinfo_area']['base_area']:
                            base_items = i['baseinfo_area']['base_area']['items']
                            for base_item in base_items:
                                base_item = base_item[0]
                                # print base_item
                                # print base_item['title']
                                if '面积'.encode('utf8') == base_item['title']:
                                    item['rentable_area'] = base_item['content']
                                if '类型'.encode('utf8') == base_item['title']:
                                    item['property_type'] = base_item['content']
                                if '临近'.encode('utf8') == base_item['title']:
                                    item['approach'] = base_item['content']
                    region = ''
                    if 'mapAddress_area' in i['baseinfo_area']:
                        region = i['baseinfo_area']['mapAddress_area']['content']

                        if 'action' in i['baseinfo_area']['mapAddress_area']:
                            item['longitude'] = i['baseinfo_area']['mapAddress_area']['action']['lon']
                            item['latitude'] = i['baseinfo_area']['mapAddress_area']['action']['lat']
                    if not region:
                        region = region_file
                    item['region'] = region
                if 'userinfo_area' in i:
                    item['contact_name'] = i['userinfo_area']['username']
                if 'image_area' in i:
                    if 'image_list' in i['image_area']:
                        image_l = []
                        for image_list in i['image_area']['image_list']:
                            # print image_list
                            image = str(image_list).split(',')
                            if image:
                                image_l.append(image[-1])
                        item['pictures'] = image_l
            # yield Request(url='http://%s.58.com/shangpu/%sx.shtml' % (city_code, page_code),
            #               callback=self.parse_phone, meta={'item': item}, dont_filter=False)
            item['contact_phone'] = ''
        others = content_json['result'].get('other')
        if others:
            add_history = others.get('add_history')
            if add_history:
                item['right_keyword'] = add_history.get('right_keyword')

        print item
        return item


# def parse_phone(self, response):
#     item = response.meta['item']
#     sel = Selector(response)
#     phone = sel.xpath('//span[@class="phone"]/text()').extract()
#     if phone:
#         phone = ''.join(phone).replace('\r', '').replace('\t', '').replace('\n', '').strip()
#         item['contact_phone'] = phone
#
#     yield item

def get_json_hierarchy(_json_obj, arch_ele_list):
    for e in arch_ele_list:
        if e not in _json_obj:
            return None
        _json_obj = _json_obj[e]
    return _json_obj


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


uid_set = set()
for line in sys.stdin:
    line = json.loads(line)
    content1 = line
    content = tranform_content(content1['body_content'], content1['city_name'], content1['city_code'],
                               content1['region'], content1['detail_url'], content1['start_time'])
    result = []
    result.append(get_json_hierarchy(content, ['detail_url']))
    result.append(get_json_hierarchy(content, ['city']))
    result.append(get_json_hierarchy(content, ['title']))
    result.append(json.dumps(get_json_hierarchy(content, ['pictures'])))
    result.append(get_json_hierarchy(content, ['region']))
    result.append(get_json_hierarchy(content, ['describe']))

    result.append(get_json_hierarchy(content, ['longitude']))
    result.append(get_json_hierarchy(content, ['approach']))
    result.append(get_json_hierarchy(content, ['rentable_area']))
    result.append(get_json_hierarchy(content, ['pubtime']))
    result.append(get_json_hierarchy(content, ['latitude']))

    result.append(get_json_hierarchy(content, ['contact_name']))
    result.append(get_json_hierarchy(content, ['property_type']))
    result.append(get_json_hierarchy(content, ['contact_phone']))
    result.append(get_json_hierarchy(content, ['rent']))
    result.append(get_json_hierarchy(content, ['tasktime']))
    result.append(get_json_hierarchy(content, ['right_keyword']))
    result.append(get_json_hierarchy(content, ['tasktime']))
    print "\t".join(format_list(result))


    
    