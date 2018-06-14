# -*- coding: utf-8 -*-
import json
import re
import urllib

import web

from dianpingdoctor.items import DianpingdoctorItem
import scrapy


class DoctorSpider(scrapy.Spider):
    name = "doctor"
    allowed_domains = ["dianping.com"]
    # start_urls = ['http://dianping.com/']

    def start_requests(self):
        db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
        data = db.query("select shop_id,shop_name from t_hh_dianping_shop_info_pet_hospital where shop_id not in ('0','1','2','3','6','7','8') group by shop_id,shop_name;")
        for d in data:
            shop_id = d.get('shop_id')
            shop_name = d.get('shop_name')
            url = 'https://m.dianping.com/easylife/node/html/techlist.html?techniciantype=201&companytype=1&shopid='+ str(shop_id)
            # url = 'https://m.dianping.com/easylife/node/html/techdetail.html?techniciantype=201&id=1635089&shopid=73572714'
            header = {
                'Host': 'm.dianping.com',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
            }
            yield scrapy.Request(url,callback=self.parse,headers=header,meta={'shop_name':shop_name})

    def parse(self, response):
        content = response.body
        data = re.findall('push\(JSON\.parse\(decodeURIComponent\("(.*?)"\)', content)
        if data:
            data = urllib.unquote(''.join(data))
            item = DianpingdoctorItem()
            print data
            data_json = json.loads(data)
            print data_json
            props = data_json.get('props')
            if props:
                shopname = response.meta.get('shop_name')
                item['shopname'] = shopname
                shopid = props.get('shopid')
                item['shopid'] = shopid
                techList = props.get('techList')
                if techList:
                    for tech in techList:
                        skills = tech.get('skills')
                        item['skills'] = skills
                        doctor_id = tech.get('id')
                        item['doctor_id'] = doctor_id
                        title =tech.get('title')
                        item['title'] = title
                        name = tech.get('name')
                        item['name'] = name
                        isCertified = tech.get('isCertified')
                        item['isCertified'] = isCertified
                        isVoted = tech.get('isVoted')
                        item['isVoted'] = isVoted
                        workYear = tech.get('workYear')
                        item['workYear'] = workYear
                        avatar = tech.get('avatar')
                        item['avatar'] = avatar
                        voteCount = tech.get('voteCount')
                        item['voteCount'] = voteCount
                        briefDesc = tech.get('briefDesc')
                        item['briefDesc'] = briefDesc
                        yield item

