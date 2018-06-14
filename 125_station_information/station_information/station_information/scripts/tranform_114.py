# coding=utf8

import sys
from lxml import etree
import json


def extract_str(str_):
    str_ = str_.replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '')
    return str_


def parse(line):
    result = {}
    content = json.loads(line)
    content = content.get('content')
    selector = etree.HTML(content)
    train_number = ''.join(selector.xpath('//div[@class="checimessage clearfix"]/dl/dt/h1/text()'))
    result['train_number'] = train_number
    checi_type = ''.join(selector.xpath('//div[@class="checimessage clearfix"]/dl/dt/p/text()'))
    train_class_name = extract_str(checi_type)
    result['train_class_name'] = train_class_name
    info_list = selector.xpath('//div[@class="checimessage clearfix"]/dl/dd/ul/li')
    if info_list:
        start_station_name = extract_str(info_list[0].xpath('string()'))
        end_station_name = extract_str(info_list[1].xpath('string()'))
        start_time = extract_str(info_list[2].xpath('string()'))
        end_time = extract_str(info_list[3].xpath('string()'))
        whole_journey = extract_str(info_list[4].xpath('string()'))
        all_time = extract_str(info_list[5].xpath('string()'))
        result['start_station_name'] = start_station_name
        result['end_station_name'] = end_station_name
        result['start_time'] = start_time
        result['end_time'] = end_time
        result['whole_journey'] = whole_journey
        result['all_time'] = all_time
    station_info_list = selector.xpath('//div[@class="list"]/table/tr')
    if station_info_list:
        for station_info in station_info_list:
            station_tr_list = station_info.xpath('./td')
            if len(station_tr_list)>3:
                station_no = extract_str(station_tr_list[0].xpath('string()'))
                result['station_no'] = station_no

                station_name = extract_str(station_tr_list[1].xpath('string()'))
                result['station_name'] = station_name

                arrival_time = extract_str(station_tr_list[2].xpath('string()'))
                result['arrival_time'] = arrival_time

                departure_time = extract_str(station_tr_list[3].xpath('string()'))
                result['departure_time'] = departure_time

                mileage = extract_str(station_tr_list[4].xpath('string()'))
                result['mileage'] = mileage
    print json.dumps(result)





for line in sys.stdin:
    parse(line)
