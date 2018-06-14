# -*- coding: utf-8 -*-
import scrapy
import urllib
import datetime
import random
import string
from hillinsight.storage import dbs
from shuaqi.items import NipponItem

class ShuaqiSpider(scrapy.Spider):
    name = "shuaqi_sp"
    allowed_domains = ["nipponpaint.com.cn"]
    dt = ""

    def __init__(self):
        self.dt = datetime.datetime.now().strftime("%Y-%m-%d")
        self.dt_last_day = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

    def start_requests(self):

        return [ scrapy.http.Request(
            url = "http://shuaxinfuwu.nipponpaint.com.cn/api/GetPersonHandler.ashx?d=" + urllib.parse.quote(datetime.datetime.now().strftime("%a %b %d %Y %H:%M:%S GMT+0800 ")+'(中国标准时间)'),
            method = "POST",
            headers = {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "shuaxinfuwu.nipponpaint.com.cn",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            },
            body = "p5=12&p6=1") ]

    def parse(self, response):
        total_page_num = int(response.xpath("//R/@A0")[0].extract())
        for page_num in range(1, total_page_num+1):
            yield scrapy.http.Request(
                url="http://shuaxinfuwu.nipponpaint.com.cn/api/GetPersonHandler.ashx?d=" + urllib.parse.quote(
                    datetime.datetime.now().strftime("%a %b %d %Y %H:%M:%S GMT+0800 ") + '(中国标准时间)'),
                method = "POST",
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Host": "shuaxinfuwu.nipponpaint.com.cn",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                },
                body = "p5=12&p6={page_num}".format(page_num=page_num),
                dont_filter = True,
                callback = self.parse_list
            )

    def parse_list(self, response):
        ids = [ id for id in response.xpath("//R/I/@A5").extract() ]
        db = dbs.create_engine("hillinsight", online=True, master=False)
        sql = "select id from hillinsight.paint where id in ('" + "','".join(ids) + "') and getdate >= '{dt}'".format(dt = self.dt_last_day)
        ready_ids = [ row["id"] for row in db.query(sql) ]
        for id in [ id for id in ids if id not in ready_ids]:
            yield scrapy.http.Request(
                url = "http://shuaxinfuwu.nipponpaint.com.cn/api/GetSinglePersonHandler.ashx?r={rand1}.{rand2}".format(
                    rand1 = "".join([random.choice(string.digits) for _ in range(3)]),
                    rand2 = "".join([random.choice(string.digits) for _ in range(13)])),
                method = "POST",
                headers = {
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "Host": "shuaxinfuwu.nipponpaint.com.cn",
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
                },
                body = "p1={id}".format(id=id),
                dont_filter = True,
                callback = self.parse_detail
            )

    def parse_detail(self, response):
        item = NipponItem()
        tmp = response.xpath("//R/I/@A8")
        item["status"] = tmp[0].extract() if len(tmp) > 0 else ""
        tmp = response.xpath("//R/I/@A3")
        item["province"] = tmp[0].extract() if len(tmp) > 0 else ""
        tmp = response.xpath("//R/I/@A0")
        item["name"] = tmp[0].extract() if len(tmp) > 0 else ""
        tmp = response.xpath("//R/I/@A4")
        item["city"] = tmp[0].extract() if len(tmp) > 0 else ""
        tmp = response.xpath("//R/I/@A1")
        item["gender"] = tmp[0].extract() if len(tmp) > 0 else ""
        tmp = response.xpath("//R/I/@A7")
        item["level"] = tmp[0].extract() if len(tmp) > 0 else ""
        tmp = response.xpath("//R/I/@A6")
        item["custom"] = tmp[0].extract() if len(tmp) > 0 else 0
        tmp = response.xpath("//R/I/@A5")
        item["time"] = tmp[0].extract() if len(tmp) > 0 else ""
        tmp = response.xpath("//R/I/@A2")
        item["id"] = tmp[0].extract() if len(tmp) > 0 else ""
        item["company"] = "nippon"
        item["getdate"] = self.dt
        yield item


    
    
    
    