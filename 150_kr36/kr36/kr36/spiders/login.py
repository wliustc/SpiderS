# -*- coding: utf-8 -*-
import scrapy
import time
import random


class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["rong.36kr.com"]

    def start_requests(self):
        url = 'https://passport.36kr.com/pages/?ok_url=https%3A%2F%2Frong.36kr.com%2F#/login'
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'passport.36kr.com',
            'Referer': 'https://rong.36kr.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

        yield scrapy.Request(url, headers=header, dont_filter=True)

    def parse(self, response):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'passport.36kr.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        yield scrapy.FormRequest(url='https://passport.36kr.com/passport/sign_in    ', formdata={
            'type': 'login',
            'bind': 'false',
            'needCaptcha': 'false',
            'username': '18210193504',
            'password': '111111',
            'ok_url': 'https%3A%2F%2Frong.36kr.com%2F',
            'ktm_reghost': 'rong.36kr.com',
        }, headers=header, callback=self.login_test, dont_filter=True)

    def login_test(self, response):
        url = 'https://rong.36kr.com/api/user/identity'

        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'rong.36kr.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }

        yield scrapy.Request(url,headers=header,callback=self.home_api,dont_filter=True )


    def home_api(self,response):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'rong.36kr.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        ll = [('123GO', '36027443'), ('Hyper', '131622'), ('Abundy', '11229541'), ('Anki', '93956175'),
              ('Clearpath Robotics', '81752055'), ('Clover Health', '46907976'), ('drive.ai', '99672904'),
              ('Graphcore', '87936558'), ('Petuum', '32473066'), ('Quantifind', '29506735'), ('Rulai', '21344670'),
              ('StreamSets', '48319787'), ('VoxelCloud', '164898'), ('Zest Finance', '90548470'), ('Zoox', '82864515')]

        for key in ll:
            url = 'https://rong.36kr.com/n/api/company/{}/finance'
            time_deco = random.randint(10, 40)
            time.sleep(time_deco)
            url = url.format(str(key[1]))

            yield scrapy.Request(url, headers=header, callback=self.login_end, dont_filter=True, meta={'name': key[0]})

    def login_end(self, response):
        # with open('test.html','a') as f:
        #     f.write(str(response.body))
        item = {}
        item['data'] = response.body
        item['company_name'] = response.meta.get('name')
        yield item



