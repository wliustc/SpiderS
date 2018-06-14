# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyanchaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class QiDuoWeiItem(scrapy.Item):
    response_body = scrapy.Field()


class ProtectiveFoodsItem(scrapy.Item):
    company_name = scrapy.Field()
    license_number = scrapy.Field()
    legal_representative = scrapy.Field()
    address = scrapy.Field()
    permissive_range = scrapy.Field()
    licence_issuing_authority = scrapy.Field()
    date_of_issue = scrapy.Field()
    valid_date = scrapy.Field()
    state_of_certificate = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    district = scrapy.Field()
    link = scrapy.Field()
    write_time = scrapy.Field()
    # response_body = scrapy.Field()
    # url = scrapy.Field()

class LicensedPharmacistItem(scrapy.Item):
    name = scrapy.Field()
    qualification_certificate_number = scrapy.Field()
    sex = scrapy.Field()
    practice_units_name = scrapy.Field()
    registered_certificate_number = scrapy.Field()

class PharmacistItem(scrapy.Item):
    name = scrapy.Field()
    qualification_certificate_number = scrapy.Field()
    sex = scrapy.Field()
    practice_units_name = scrapy.Field()

class DrugAdvertisementItem(scrapy.Item):
    advertisement_approve_number = scrapy.Field()
    use_name = scrapy.Field()
    approve_date = scrapy.Field()
    expiry_date = scrapy.Field()

class AdministrativePenaltyItem(scrapy.Item):
    administrative_penalty_decision_number = scrapy.Field()
    legal_case_name = scrapy.Field()
    party_name = scrapy.Field()
    organization_code = scrapy.Field()
    legal_representative = scrapy.Field()
    main_facts = scrapy.Field()
    legal_basis = scrapy.Field()
    methods_of_performance = scrapy.Field()
    penalty_organ = scrapy.Field()
    