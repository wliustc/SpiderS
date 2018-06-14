# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdpaintItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    brand_name=scrapy.Field()
   # brand_id=scrapy.Field()
    #shop_id=scrapy.Field()
    shop_name=scrapy.Field()
    shop_id=scrapy.Field()
    shop_type=scrapy.Field()
    ware_id=scrapy.Field()
    ware_name=scrapy.Field()
    price=scrapy.Field()
    comment_count=scrapy.Field()#评论次数
    address=scrapy.Field()#发货地址
    volume=scrapy.Field()
    units=scrapy.Field()
    task_date=scrapy.Field()
    pass
