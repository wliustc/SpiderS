# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import json
import time
import re
from tx_shippin.items import TxShipinItem
class FenleiSpider(scrapy.Spider):
    name = "fenlei"
    allowed_domains = ["v.qq.com"]

    def start_requests(self):
        url='http://v.qq.com/x/list/movie'
        header={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.9',
            'Cache-Control':'max-age=0',
            'Host':'v.qq.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        yield scrapy.Request(url,headers=header,
                       dont_filter=True,callback=self.get_1list)


    def get_1list(self, response):
        temps=response.css('.filter_list a')
        for temp in temps:
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Host': 'v.qq.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            }
            url=temp.css('a::attr("href")').extract()[0]
            type=temp.css('a::text').extract()[0]
            # '音乐', '新闻', '娱乐', '体育', '游戏', '搞笑', '王者荣耀', '时尚', '生活', '母婴', '汽车', '科技',
            # '教育', '财经', '房产', '旅游'
            yield scrapy.Request(url, headers=header,
                                 dont_filter=True, meta={'item':{'type':type},'base_url':url,'page':0,'page_zongji':0},callback=self.get_2list)

    def get_2list(self, response):
        page=response.meta['page']
        page_gong=response.meta['page_zongji']
        base_url=response.meta['base_url']
        if page_gong == 0:
            page_gong = int(''.join(response.css('.filter_option .option_txt::text').extract()).split('/')[-1])
        page += 1
        if page_gong >= page:
            url = base_url + '?&offset=' + str(30 * page)
            header = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Host': 'v.qq.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            }
            yield scrapy.Request(url, headers=header,
                                 dont_filter=True, meta={'base_url': base_url, 'page': page, 'page_zongji': page_gong,
                                                         'item':{'type':response.meta['item']['type']}},
                                 callback=self.get_2list)
        if response.meta['item']['type'] in ['电影', '电视剧', '综艺', '动漫', '少儿','纪录片','微电影']:
            temps = response.css('.figures_list li')
            for temp in temps:
                item=TxShipinItem()
                item['url'] = temp.css('a::attr("href")').extract()[0]
                item['item_id'] = temp.css('a::attr("data-float")').extract()[0]
                item['type'] = response.meta['item']['type']
                item['title'] = temp.css('.figure_title_score .figure_title a::text').extract()[0]
                try:
                    item['count'] = temp.css('.figure_count span::text').extract()[0]
                except Exception as e:
                    item['count']=''
                item['score'] = ''.join(temp.css('.figure_title_score .figure_score em::text').extract())
                item['floor'] = '腾讯视频'
                item['dubo'] = 0
                item['zizhi'] = 0
                try:
                    tag = temp.css('a i.mark_v img::attr("alt")').extract()[0]
                    if tag == '独播':
                        item['dubo'] = 1
                    elif tag == '腾讯出品':
                        item['zizhi'] = 1
                except Exception as e:
                    pass
                if response.meta['item']['type'] in ['电影','电视剧','动漫','少儿','纪录片','微电影']:
                    header = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache-Control': 'max-age=0',
                        'Host': 'node.video.qq.com',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
                    }
                    '.figure_caption .figure_info'
                    url='http://node.video.qq.com/x/api/float_vinfo2?cid='+item['item_id']
                    yield scrapy.Request(url, headers=header,
                                         dont_filter=True, meta={'item':item},callback=self.get_item_year)
                elif response.meta['item']['type'] in ['综艺']:
                    try:
                        item['year'] = re.sub('[^0-9\-]','',temp.css('.figure_caption .figure_info::text').extract()[0]).split('-')[0]
                    except Exception as e:
                        item['year'] = ''
                    item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
                    yield item
        elif response.meta['item']['type'] in ['音乐','新闻','娱乐','体育','游戏','搞笑','王者荣耀','时尚','生活','母婴','汽车','科技',
                                               '教育','财经','房产','旅游']:
            temps = response.css('.mod_figures .list_item')
            for temp in temps:
                item=TxShipinItem()
                item['url'] = temp.css('a::attr("href")').extract()[0]
                item['item_id'] = temp.css('::attr("__wind")').extract()[0].split('=')[-1]
                item['type'] = response.meta['item']['type']
                item['title'] = temp.css('.figure_title a::attr("title")').extract()[0]
                try:
                    item['count'] = re.search('class=\"num\">(?P<name>.+)<',temp.xpath('./comment()').extract()[0]).groupdict()['name']
                except Exception as e:
                    item['count']=''
                item['floor'] = '腾讯视频'
                item['dubo'] = 0
                item['zizhi'] = 0
                item['year']=''
                item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
                yield item
    def get_item_year(self, response):
        item=response.meta['item']
        data=json.loads(response.body.decode())
        item['year']=data['c']['year']
        item['dt'] = time.strftime('%Y-%m-%d', time.localtime())
        yield item


    
    
    
    
    
    
    
    
    
    
    