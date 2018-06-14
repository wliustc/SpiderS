# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LoanListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    loan_id = scrapy.Field()
    city = scrapy.Field()
    dt = scrapy.Field()
    loan_type = scrapy.Field()
    loan_name = scrapy.Field()
    loan_duration = scrapy.Field()
    loan_amt = scrapy.Field()
    interest = scrapy.Field()
    total_expense = scrapy.Field()
    month_expense = scrapy.Field()
    day_expense = scrapy.Field()
    once_add = scrapy.Field()
    month_add = scrapy.Field()
    month_interest_rate = scrapy.Field()
    interest_expense = scrapy.Field()
    add_expense = scrapy.Field()
    once_add_expense = scrapy.Field()
    mortgage_info = scrapy.Field()
    lending_time_info = scrapy.Field()
    identity_limit_info = scrapy.Field()
    prepayment_requirement = scrapy.Field()
    extra_info = scrapy.Field()
    requirement_detail = scrapy.Field()
    created_time = scrapy.Field()

    pass
