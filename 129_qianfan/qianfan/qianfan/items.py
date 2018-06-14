# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
class QianfanDetailItem(scrapy.Item):
    content = scrapy.Field()
    meta = scrapy.Field()

class QianfanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    dateValue = scrapy.Field()
    activeNums = scrapy.Field()
    activeAvgDay = scrapy.Field()
    runtimeAvgPersonRatio = scrapy.Field()
    arithId = scrapy.Field()
    activeAvgDayRatio = scrapy.Field()
    developCompanyAbbr = scrapy.Field()
    launchAvgDayRatio = scrapy.Field()
    cateName = scrapy.Field()
    launchNums = scrapy.Field()
    concern = scrapy.Field()
    publishCompanyAbbr = scrapy.Field()
    launchAvgPersonRatio = scrapy.Field()
    runtimeAvgDay = scrapy.Field()
    appId = scrapy.Field()
    publishCompanyId = scrapy.Field()
    runtimeNums = scrapy.Field()
    catePermeability = scrapy.Field()
    launchPerPersonRatio = scrapy.Field()
    statDate = scrapy.Field()
    appName = scrapy.Field()
    developCompanyId = scrapy.Field()
    isDisplay = scrapy.Field()
    runtimeNumsRatio = scrapy.Field()
    publishCompanyFullName = scrapy.Field()
    runtimePerPersonRatio = scrapy.Field()
    launchAvgDay = scrapy.Field()
    cateId = scrapy.Field()
    activeNumsRatio = scrapy.Field()
    launchAvgPerson = scrapy.Field()
    developCompanyFullName = scrapy.Field()
    launchNumsRatio = scrapy.Field()
    runtimeAvgPerson = scrapy.Field()
    runtimePerPerson = scrapy.Field()
    runtimeAvgDayRatio = scrapy.Field()
    launchPerPerson = scrapy.Field()

    
class QianfanCustomizationItem(scrapy.Item):
    content = scrapy.Field()
    meta = scrapy.Field()
    category_type = scrapy.Field()

    
    