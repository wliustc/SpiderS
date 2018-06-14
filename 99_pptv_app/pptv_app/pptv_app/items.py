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
    city = scrapy.Field()
    competition = scrapy.Field()
    place = scrapy.Field()
    registration_time = scrapy.Field()
    attend = scrapy.Field()
    pt_jobid = scrapy.Field()
    #黑鸟活动
    activity_id = scrapy.Field()
    title = scrapy.Field()
    route = scrapy.Field()
    abort = scrapy.Field()
    startTime = scrapy.Field()
    endTime = scrapy.Field()
    sign_up = scrapy.Field()
    #黑鸟车队
    teamId = scrapy.Field()
    teamName = scrapy.Field()
    teamCode = scrapy.Field()
    teamSlogon = scrapy.Field()
    active = scrapy.Field()
    number = scrapy.Field()
    cityId = scrapy.Field()
    cityName = scrapy.Field()
    #聚力热门
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




