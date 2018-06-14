# -*- coding: utf-8 -*-
import scrapy
import re
import os

_mapping = {'item_id': re.compile(r'/product-reviews/(\w+)/'),
            'next_page': re.compile(r'pageNumber=(\d+)')}
_current_dir = os.path.abspath(".")
def get_urls():
    urls = []
    url_file = '/tmp/urls.txt'
    with open(url_file) as f:
        while True:
            line = f.readline().strip()
            if not line:
                break
            urls.append(line)
    return urls

def get_regex_group1(key, _str, default=None):
    p = _mapping[key]
    m = p.search(_str)
    if m:
        return m.group(1)
    return default



def format_rate(rate):
    try:
        if not rate:
            return '0.0'
        r = rate.split(" ")
        if len(r) > 0:
            return r[0]
        else:
            return rate[0:3]
    except:
        return '0.0'

def format_date(date):
    try:
        if not date:
            return '0000-00-00'
        date_dic = {"January": "1", "February": "2", "March": "3", "April": "4", "May": "5", "June": "6", "July": "7",
                    "August": "8", "September": "9", "October": "10", "November": "11", "December": "12"}
        r = date.split(",")
        pres = r[0].strip().split(" ")
        m = date_dic[pres[1]]
        d = pres[2]
        y = r[1].strip()
        return "%s-%s-%s" % (y, m, d)
    except:
        return '0000-00-00'

class AmazonSpider(scrapy.Spider):
    name = "amazon_pet_review"
    allowed_domains = ["amazon.com"]
    start_urls = get_urls()
    count = 0

    def parse(self, response):
        selectors = response.xpath("//*[@id='cm_cr-review_list']//*[@data-hook='review']")
        if len(selectors) > 0:
            next_page_num = int(get_regex_group1('next_page', response.url)) + 1
            next_url = re.sub('pageNumber=\d+', 'pageNumber={}'.format(next_page_num), response.url)
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

        for sel in selectors:
            item_id = get_regex_group1('item_id', response.url)
            title = response.xpath(
                '//*[@id="cm_cr-product_info"]//*[contains(@data-hook,"product-link")]/text()').extract()
            brand_name = response.xpath('//*[contains(@class,"product-by-line")]/a/text()').extract()
            rate = sel.xpath("div/a/i/span/text()").extract()
            date = sel.xpath("./div//*[contains(@data-hook,'review-date')]/text()").extract()
            review = sel.xpath('./div//*[contains(@data-hook,"review-body")]/text()').extract()
            item = {}
            item['item_id'] = item_id
            item['title'] = title[0] if title else ''
            item['brand_name'] = brand_name[0] if brand_name else ''
            item['rate'] = rate[0] if rate else ''
            item['rate'] = format_rate(item['rate'])
            item['date'] = date[0] if date else ''
            item['date'] = format_date(item['date'])
            item['review'] = review[0] if review else ''
            self.count += 1
            if self.count % 10 == 0:
                print "get %s items" % self.count
            yield item


