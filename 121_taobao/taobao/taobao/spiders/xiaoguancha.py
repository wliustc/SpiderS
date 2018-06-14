# -*- coding: utf-8 -*-
import json
import sys
import scrapy
import re
from taobao.items import TaobaoItem

from scrapy import Request

reload(sys)
sys.setdefaultencoding("utf-8")

header = {
    'Host': 'detail.tmall.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0'
}

# db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class XiaoguanchaSpider(scrapy.Spider):
    name = "xiaoguancha"
    allowed_domains = ["taobao.com", 'tmall.com']
    start_urls = [
        # 'https://xiaoguantea.tmall.com/i/asynSearch.htm?_ksTS=1504766891115_116&callback=jsonp117&mid=w-14994389364-0&wid=14994389364&path=/category.htm',
        'https://detail.tmall.com/item.htm?id=539330211018&rn=677d52305b3bcf3853d4aca'
        'e22515a0c&abbucket=0&on_comment=1#J_TabBar'
    ]

    def start_requests(self):
        # url = 'https://detail.tmall.com/item.htm?id=537613974917'
        # yield Request(url,callback=self.parse_detail,dont_filter=True,
        # meta={'title':'title','price':'price','sale_num':'sale_num','comment_num':'comment_num'})
        url = 'https://xiaoguantea.tmall.com/i/asynSearch.htm?_ksTS=1504766891115_116' \
              '&callback=jsonp117&mid=w-14994389364-0&wid=14994389364&path=/category.htm'
        yield Request(url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        content = response.body.replace('\"', '"')
        content = content.replace('\\\"', '"')
        # print response.body
        # self.write_file(content)
        pattern = 'item-name J_TGoldData"[\s\S]*?href="(.*?)" target="_blank"[\s\S]*?' \
                  'data-gold-data=[\s\S]*?>(.*?)</a>[\s\S]*?class="c-price">' \
                  '([\s\S]*?)</span></div>[\s\S]*?class="sale-num">(\d+)</span>'
        result_list = re.findall(pattern, content)
        if result_list:

            for result in result_list:
                detail_url = result[0]
                title = result[1]
                price = result[2]
                sale_num = result[3]
                url = 'https:' + detail_url
                url = url.split('&')[0]
                yield Request(url, callback=self.parse_detail, meta={
                    'detail_url': url,
                    'title': title.decode('gbk').strip(),
                    'price': price,
                    'sale_num': sale_num
                }, dont_filter=True, headers=header)

    def parse_comment_num(self, response):
        content = response.body
        rateTotal = ''.join(re.findall('rateTotal":(\d+),', content))

        meta = response.meta
        id = meta['id']
        spuId = meta['spuId']
        sellerId = meta['sellerId']
        meta['comment_num'] = rateTotal
        url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=%s&spuId=%s' \
              '&sellerId=%s&order=3&append=0&content=1&tagId=&posi=&picture=&callback=json&currentPage=1' % (
                  id, spuId, sellerId)
        yield Request(url, callback=self.parse_comment, meta=meta, dont_filter=True)

    def write_file(self, data):
        with open('dddpd', 'a') as f:
            f.write(data)

    def parse_detail(self, response):
        meta = response.meta
        spuId = re.findall('spuId=(\d+)&', response.body)
        if spuId:
            spuId = spuId[0]
        else:
            spuId = re.findall('spuId":"(\d+)"', response.body)
            if spuId:
                spuId = spuId[0]
        id = re.findall('itemId":"(\d+)"', response.body)
        if id:
            id = id[0]
        sellerId = re.findall('sellerId:"(\d+)"', response.body)
        if sellerId:
            sellerId = sellerId[0]
        print spuId, id, sellerId
        print '---' * 10
        if spuId and id and sellerId:
            url = 'https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=%s&spuId=%s&sellerId=%s&callback=json'
            meta['currentPage'] = 1
            meta['spuId'] = spuId
            meta['id'] = id
            meta['sellerId'] = sellerId
            yield Request(url, callback=self.parse_comment_num, meta=meta, dont_filter=True)
        else:
            yield Request(response.url, callback=self.parse_detail, meta=meta, dont_filter=True)
            # pass

    def parse_comment(self, response):
        meta = response.meta
        content = response.body
        pattern = 'displayUserNick":"(.*?)",.*?"rateContent":"(.*?)","rateDate":"(.*?)"'
        data = re.findall(pattern, content)
        if data:
            for d in data:
                item = TaobaoItem()
                displayUserNick = d[0]
                rateContent = d[1]
                rateDate = d[2]
                item['displayUserNick'] = displayUserNick
                item['rateContent'] = rateContent
                item['rateDate'] = rateDate
                item['title'] = meta['title']
                item['price'] = meta['price']
                item['sale_num'] = meta['sale_num']
                item['comment_num'] = meta['comment_num']
                item['comment_url'] = response.url
                item['detail_url'] = meta['detail_url']
                yield item
            if len(data) == 20:
                url = response.url
                currentPage = meta['currentPage']
                currentPage += 1
                url = url.split('&currentPage=')[0]
                url = url + '&currentPage=%s' % currentPage
                meta['currentPage'] = currentPage
                yield Request(url, callback=self.parse_comment, meta=meta, dont_filter=True)





                # content = content[8:-1]
                #
                # conten_json = json.loads(content, encoding='gbk')
                # rateDetail = conten_json.get('rateDetail')
                # meta = response.meta
                # if rateDetail:
                #     rateList = rateDetail.get('rateList')
                #     if rateList:
                #
                #         item['comment_list'] = rateList
                #         item['title'] = meta['title']
                #         item['price'] = meta['price']
                #         item['sale_num'] = meta['sale_num']
                #         item['comment_num'] = meta['comment_num']
                #         item['comment_url'] = response.url
                #         item['detail_url'] = meta['detail_url']
                #         yield item
                #
                #     if len(rateList) == 20:
                #         url = response.url
                #         currentPage = meta['currentPage']
                #         currentPage += 1
                #         url = url.split('&currentPage=')[0]
                #         url = url + '&currentPage=%s' % currentPage
                #         meta['currentPage'] = currentPage
                #         yield Request(url, callback=self.parse_comment, meta=meta, dont_filter=True)
                #
