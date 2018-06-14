# -*- coding: utf-8 -*-
import scrapy
import json
import random
import re
import time
from dentist_invisalign.items import DentistInvisalignItem

def from_bytes (data, big_endian = False):
    if isinstance(data, str):
        data = bytearray(data)
    if big_endian:
        data = reversed(data)
    num = 0
    for offset, byte in enumerate(data):
        num += byte << (offset * 8)
    return num

def GenerateShortGuid():
	return GenerateRandom("xxxxxxxxxxxx")

def GenerateRandom(e):
    def a(e):
        t = 16 * random.random()
        e=e[0]
        if "x" == e:
            a = int(t)
        else:
            a = 8 | 3 & int(t)

        return change10_to_36(a)
    e=re.sub('[xy]',a,e)
    return e
def get_token(a,b,c):
    d=[None]*len(b)

    for e in range(0,len(b)):
        d[e] = from_bytes(b[e].encode(),'big')
    d.insert(0,c)
    b = 0
    e = len(d)
    for c in range(0,e):
        b *= 1729
        b += d[c]
        b %= a
    return b

def change10_to_36(n):
    loop = '0123456789abcdefghijklmnopqrstuvwxyz'
    a=[]
    while n != 0:
        a.append(loop[n % 36])
        n = n // 36
    a.reverse()
    out = ''.join(a)  # out:'hzqhoyh9'
    return out

class DentistSpider(scrapy.Spider):
    name = "dentist"
    allowed_domains = ["www.invisalign.com"]

    def start_requests(self):
        for i in range(0,100000):
            code="%05i" % i
            url="https://maps.googleapis.com/maps/api/js/GeocodeService.Search?4s%2C%20%20"+str(i)+\
                "%2C%20US&7sUS&9szh-CN&client=gme-aligntechnologyinc"
            temp=get_token(2147483647,url,0)
            call_back=change10_to_36(temp)
            url=url+'&callback=_xdc_.'+call_back
            tmp = re.search("(?:https?:\/\/[^\/]+)?(.*)", url)
            tmp = get_token(131071, tmp[1], 201048313)
            url = url + '&token=' + str(tmp)
            yield scrapy.Request(url,headers={
                'accept':'*/*',
                'accept-encoding':'gzip, deflate, sdch, br',
                'accept-language':'zh-CN,zh;q=0.8',
                'x-client-data':'CKW1yQEIjbbJAQijtskBCMG2yQEI+pzKAQipncoBCMqeygE=',
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            },meta={'item':{'search_id':i}},dont_filter=True)


    def parse(self, response):
        tmp=re.search('(?:{([^\)])+)',response.body.decode())
        tmp=json.loads(tmp[0])
        yield scrapy.FormRequest(
                    'https://api.invisalign.com/svc/rd',
                    method='GET',
                    formdata={
                        'pc':str(response.meta['item']['search_id']),
                        'usa':'',
                        'uct':'',
                        'ust':'',
                        'cl':'US',
                        'fn':'',
                        'f':'F1,ft',
                        's':'S4',
                        'rd':'10',
                        'rdi':'2.5',
                        'it':'us',
                        'pst':'1',
                        'lat':str(tmp['results'][0]['geometry']['location']['lat']),
                        'lng':str(tmp['results'][0]['geometry']['location']['lng']),
                        'cid':GenerateShortGuid(),
                        'sid':GenerateShortGuid(),
                        'vid':GenerateShortGuid(),
                        '_':str(round(time.time() * 1000)),
                    },
                    callback=self.get_dentist,dont_filter=True,meta={'code':response.meta['item']['search_id']}
        )


    def get_dentist(self, response):
        data=json.loads(response.body)
        results=data['responseData']['results']
        for result in results:
            item=DentistInvisalignItem()
            item.update(result)
            item['dt']=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            item['code'] = response.meta['item']['code']
            yield item



    