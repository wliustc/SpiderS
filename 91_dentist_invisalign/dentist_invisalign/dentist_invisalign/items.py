# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DentistInvisalignItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Accuracy= scrapy.Field()
    AnnotationList= scrapy.Field()
    City= scrapy.Field()
    Country= scrapy.Field()
    Distance= scrapy.Field()
    DocID= scrapy.Field()
    DoctorType= scrapy.Field()
    Fax= scrapy.Field()
    FirstName= scrapy.Field()
    FullName= scrapy.Field()
    HasAdditionalLocations= scrapy.Field()
    HasBio= scrapy.Field()
    HasEmail= scrapy.Field()
    IsCABMember= scrapy.Field()
    IsFacultyMember= scrapy.Field()
    IsItero= scrapy.Field()
    IsTeenDoctor= scrapy.Field()
    IsTeenGuarantee= scrapy.Field()
    IsVip= scrapy.Field()
    LastName= scrapy.Field()
    Latitude= scrapy.Field()
    Line1= scrapy.Field()
    Line2= scrapy.Field()
    Line3= scrapy.Field()
    Line4= scrapy.Field()
    Longitude= scrapy.Field()
    Num= scrapy.Field()
    OfficePhone= scrapy.Field()
    PostalCode= scrapy.Field()
    SegmentCode= scrapy.Field()
    State= scrapy.Field()
    Url= scrapy.Field()
    ProfilePhoto= scrapy.Field()
    dt= scrapy.Field()
    code=scrapy.Field()
