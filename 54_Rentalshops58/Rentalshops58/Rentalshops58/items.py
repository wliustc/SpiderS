# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Rentalshops58Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    # district = scrapy.Field()
    region = scrapy.Field()
    # address = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    title = scrapy.Field()
    rent = scrapy.Field()
    pubtime = scrapy.Field()
    rentable_area = scrapy.Field()
    property_type = scrapy.Field()
    approach = scrapy.Field()
    describe = scrapy.Field()
    contact_name = scrapy.Field()
    contact_phone = scrapy.Field()
    pictures = scrapy.Field()
    # status =scrapy.Field()
    pass
