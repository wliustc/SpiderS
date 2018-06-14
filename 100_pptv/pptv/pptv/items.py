# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AppDownloadItem(scrapy.Item):
    title = scrapy.Field()
    comments = scrapy.Field()
	time = scrapy.Field()
    clubName = scrapy.Field()
    nickname = scrapy.Field()
    #聚力圈子
    remark = scrapy.Field()
    id = scrapy.Field()
    memberTotal = scrapy.Field()
    topicTotal = scrapy.Field()
    # 聚力
    create_time = scrapy.Field()
    total = scrapy.Field()
    comments_url = scrapy.Field()
    task_time = scrapy.Field()





    
    
    