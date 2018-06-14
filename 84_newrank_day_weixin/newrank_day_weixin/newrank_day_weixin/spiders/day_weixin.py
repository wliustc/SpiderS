# -*- coding: utf-8 -*-
import scrapy
import time
import execjs
import json
from newrank_day_weixin.items import NewrankItem
from newrank_day_weixin.spiders import save_js
class DayWeixin(scrapy.Spider):
    name = "day_weixin"
    allowed_domains = ["www.newrank.cn"]
    start_urls = ['http://www.newrank.cn/']
    def start_requests(self):
        init={'资讯':['时事','民生','财富','科技','创业','汽车','楼市','职场','教育','学术','政务','企业'],
              '生活':['文化','百科','健康','时尚','美食','乐活','旅行','幽默','情感','体娱','美体','文摘'],
              }
        getrandom = execjs.compile(save_js.get_random)
        myrandom = getrandom.call('h')

        dt=time.strftime('%Y-%m-%d', time.localtime(time.time() - 3600 * 24))
        for kind in init.keys():
            for i in init[kind]:
                s = '/xdnphb/list/day/rank?AppKey=joker&end=%s&rank_name=%s&rank_name_group=%s&' \
                    'start=%s&nonce=%s' %(dt,i,kind,dt,myrandom)
                get_xyz= execjs.compile(save_js.get_xyz)
                xyz=get_xyz.call('b',s)
                yield scrapy.FormRequest('http://www.newrank.cn/xdnphb/list/day/rank',
                 headers={
                     'Accept':'application/json, text/javascript, */*; q=0.01',
                     'Accept-Encoding':'gzip, deflate',
                     'Accept-Language':'zh-CN,zh;q=0.8',
                     'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                     'Host':'www.newrank.cn',
                     'Origin':'http://www.newrank.cn',
                     'Referer':'http://www.newrank.cn/public/info/list.html?period=day&type=data',
                     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
                     'X-Requested-With':'XMLHttpRequest',
                 },
                formdata={
                'end':dt,
                'rank_name':i,
                'rank_name_group': kind,
                'start': dt,
                'nonce': myrandom,
                'xyz': xyz,
                },
                meta={'item':{'start_time':dt,'end_time':dt,'group':kind,'rank':i}},
                dont_filter=True,
            )
    def parse(self, response):
        datas=json.loads(response.body)
        for data in datas['value']:
            item = NewrankItem()
            item['name']=data['name']
            item['paiming'] = data['a']
            item['account']=data['account']
            item['fabu']= data['b']+'/'+data['c']       #发布
            item['tread_num']=data['d']                 #总阅读数
            item['toutiao'] = data['e']                 #头条
            item['average'] = data['f']                 #平均
            item['max'] = data['i']                     #最高
            item['dianzan'] = data['g']                 #点赞数
            item['rank_mark'] = data['rank_mark']       #新榜指数
            item['month_top_times']=data['month_top_times']     #上榜次数
            item['start_time']=response.meta['item']['start_time']
            item['end_time'] = response.meta['item']['end_time']
            item['group']=response.meta['item']['group']
            item['rank'] = response.meta['item']['rank']
            yield item

    