# coding:utf8
import json
from lxml import etree
import sys
import time
import re
import web
reload(sys)
sys.setdefaultencoding('utf-8')
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


def tranform(lin):
    html = json.loads(lin)
    city_code = html['meta']['city_code']
    html = html['meta']['detail_content']
    content = html['content']
    data = etree.HTML(html)
    weather = ''.join(data.xpath('//div[@id="forecast"]/div[1]/div[1]/table/tbody/tr[3]/td[1]/text()'))
    sk_time = ''.join(data.xpath('/html/body/div[3]/div[1]/div[3]/span/text()')).split(u'发布于：')[1].split(' ')[0]
    data_list = []
    for i in content:
        if sk_time in i.get('time') and i.get('rain1h') != 9999.0:
            data_list.append(i)
    data_list.sort(key=lambda x: x['temperature'])
    min_temperature = data_list[0]
    max_temperature = data_list[-1]
    data_list.sort(key=lambda x: x['windSpeed'])
    min_windSpeed = data_list[0]
    max_windSpeed = data_list[-1]
    data_list.sort(key=lambda x: x['rain1h'])
    min_rain1h = data_list[0]
    max_rain1h = data_list[-1]


def tranform1(lin):
    html = json.loads(lin)
    item = {}
    city_code = html['meta']['city_code']
    # content = html['content']
    html = html['meta']['detail_content']
    data = etree.HTML(html)
    weather = ''.join(data.xpath('//div[@id="forecast"]/div[1]/div[1]/table/tbody/tr[3]/td[1]/text()'))
    sk_time = ''.join(data.xpath('/html/body/div[3]/div[1]/div[3]/span/text()'))
    temperature_data = data.xpath('//*[@id="day0"]/div[3]/div/text()')
    # temperature_ = []
    # time_s = sk_time.replace(u'发布于：', '').split(' ')[0]
    # for i in json.loads(content):
    #     if i['time'] == time_s+' 02:00' and i['temperature'] != 9999.0:
    #         temperature_.append(i['temperature'])
    #     elif i['time'] == time_s+' 08:00'and i['temperature'] != 9999.0:
    #         temperature_.append(i['temperature'])
    #     elif i['time'] == time_s+' 14:00'and i['temperature'] != 9999.0:
    #         temperature_.append(i['temperature'])
    #     elif i['time'] == time_s+' 20:00'and i['temperature'] != 9999.0:
    #         temperature_.append(i['temperature'])
    # try:
    #     averaging = "{:.1f}".format(sum(temperature_) /len(temperature_)) + r'℃'
    # except:
    temperature_ = []
    h2 = ''.join(''.join(data.xpath('//*[@id="day0"]/div[3]/div[2]/text()')).split()).replace(u'℃', '')
    h8 = ''.join(''.join(data.xpath('//*[@id="day0"]/div[3]/div[4]/text()')).split()).replace(u'℃', '')
    h14 = ''.join(''.join(data.xpath('//*[@id="day0"]/div[3]/div[6]/text()')).split()).replace(u'℃', '')
    h20 = ''.join(''.join(data.xpath('//*[@id="day0"]/div[3]/div[8]/text()')).split()).replace(u'℃', '')
    temperature_.append(float(h2))
    temperature_.append(float(h8))
    temperature_.append(float(h14))
    temperature_.append(float(h20))
    averaging = "{:.1f}".format(sum(temperature_) / len(temperature_)) + r'℃'

    temperature_list = []
    for i in temperature_data[1:]:
        i = i.split()
        if i[0] != '-':
            temperature_list.append(float(i[0][0:-1]))
    temperature_list = sorted(temperature_list)
    min_temperature = str(temperature_list[0]) + r'℃'
    max_temperature = str(temperature_list[-1]) + r'℃'
    # print min_temperature,max_temperature
    windSpeed_data = data.xpath('//*[@id="day0"]/div[5]/div/text()')
    windSpeed_list = []
    for w in windSpeed_data[1:]:
        w = ''.join(w.split()).replace(u'米/秒', '')
        if w != '-':
            windSpeed_list.append(float(w))
    windSpeed_list = sorted(windSpeed_list)
    min_windSpeed = str(windSpeed_list[0]) + '米/秒'
    max_windSpeed = str(windSpeed_list[-1]) + '米/秒'
    # print min_windSpeed,max_windSpeed
    cloudCover_data = data.xpath('//*[@id="day0"]/div[9]/div/text()')
    cloudCover_list = []
    for c in cloudCover_data[1:]:
        c = ''.join(c.split()).replace(u'%', '')
        if c != '-':
            cloudCover_list.append(float(c))
    cloudCover_list = sorted(cloudCover_list)
    min_cloudCover = str(cloudCover_list[0]) + '%'
    max_cloudCover = str(cloudCover_list[-1]) + '%'
    rain_data = data.xpath('//*[@id="day0"]/div[4]/div/text()')
    rain_list = []
    for r in rain_data[1:]:
        r = r.split()
        if u'无降水' in r[0]:
            pass
        else:
            r = r[0].replace(u'毫米', '')
            rain_list.append(float(r))
    rain_list = sorted(rain_list)
    if len(rain_list):
        min_rain = str(rain_list[0]) + '毫米'
        max_rain = str(rain_list[-1]) + '毫米'
    else:
        min_rain = '无降水'
        max_rain = '无降水'
    print city_code, min_rain, max_rain, weather, sk_time, min_temperature, max_temperature, min_windSpeed, max_windSpeed, min_cloudCover, max_cloudCover
    item['city_code'] = city_code
    item['min_rain'] = min_rain
    item['max_rain'] = max_rain
    item['weather'] = weather
    item['sk_time'] = sk_time
    item['min_temperature'] = min_temperature
    item['max_temperature'] = max_temperature
    item['min_windSpeed'] = min_windSpeed
    item['max_windSpeed'] = max_windSpeed
    item['min_cloudCover'] = min_cloudCover
    item['max_cloudCover'] = max_cloudCover
    item['averaging'] = averaging
    item['task_time'] = time.strftime("%Y-%m-%d", time.localtime())
    # item['task_time'] = '2017-11-26'
    db.insert('t_spider_weather', **item)


# 'F:\10.15.1.22_1511716207.json'
# with open(r'F:\10.15.1.22_1511716207.json','r') as f:
#     for i in f.readlines():
#         tranform1(i)
#


for i in sys.stdin:
    tranform1(i)

    