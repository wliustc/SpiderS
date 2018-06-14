# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppDownloadItem(scrapy.Item):
    source = scrapy.Field()
    app_name = scrapy.Field()
    download = scrapy.Field()
    comments = scrapy.Field()
    time = scrapy.Field()
    name = scrapy.Field()
    Appid = scrapy.Field()
    Aso_Name = scrapy.Field()
    Aso_Date = scrapy.Field()
    Aso_Downloads = scrapy.Field()
    task_time = scrapy.Field()
    pt_jobid = scrapy.Field()



    