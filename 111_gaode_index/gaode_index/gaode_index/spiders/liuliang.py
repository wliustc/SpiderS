# -*- coding: utf-8 -*-
import scrapy
import base64
import rsa
import binascii
from urllib import quote
import time
import json
import pandas as pd
import re
from map_gapde.items import MapStaticspeopleItem
from scrapy.exceptions import CloseSpider

def get_time():
    return int(time.time() * 1000)

class LiuliangSpider(scrapy.Spider):
    name = "liuliang"
    allowed_domains = ["index.amap.com"]
    start_urls = ['http://index.amap.com/']

    def encode_username(self,username):
        username=quote(username)
        bytesString = username.encode(encoding="utf-8")
        encodestr = base64.b64encode(bytesString)
        return encodestr.decode()

    def encode_password(self,password, servertime, nonce, pubkey):
        rsaPubkey = int(pubkey, 16)
        RSAKey = rsa.PublicKey(rsaPubkey, 65537)  # 创建公钥
        codeStr = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 根据js拼接方式构造明文
        pwd = rsa.encrypt(codeStr.encode(), RSAKey)  # 使用rsa进行加密
        return binascii.b2a_hex(pwd)  # 将加密信息转换为16进制。

    def get_init_task(self):    #就目前来说,对于端点续爬的问题只能依赖数据库记录和全任务对比的方式。
        import shelve
        date=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        with shelve.open(self.name+'.db') as f:
            try:
                data=f[date]
                data=pd.DataFrame(data)
                return data.sort_values('time').iloc[-1].to_dict()
            except Exception as e:
                return None

    def __init__(self):
        super(LiuliangSpider, self).__init__()

    def start_requests(self):
        url='https://api.weibo.com/oauth2/authorize?client_id=884965267&redirect_uri=https://id.amap.com/index/weibo?passport=1'
        yield scrapy.Request(url,
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Host':'api.weibo.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        },meta={"cookiejar": 1},callback=self.load_weibo_prelogin
        )

    def load_weibo_prelogin(self,response):
        username=self.encode_username('504772813@qq.com')
        url='https://login.sina.com.cn/sso/prelogin.php?entry=openapi&callback=sinaSSOController.preloginCallBack&' \
            'su='+username+'&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_='+str(get_time())
        yield scrapy.Request(url,headers={
            'Accept':'*/*',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Host':'login.sina.com.cn',
            'Referer':'https://api.weibo.com/oauth2/authorize?client_id=884965267&redirect_uri=https://id.amap.com/index/weibo?passport=1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            },
            dont_filter=True,callback=self.load_weibo_log,meta={"cookiejar": response.meta['cookiejar']})

    def load_weibo_log(self, response):
        data = re.findall('\((.+)', response.body.decode())[0].strip(')')
        data = json.loads(data)
        response_key = {}
        response_key['pubkey'] = data['pubkey']
        response_key['nonce'] = data['nonce']
        response_key['rsakv'] = data['rsakv']
        response_key['pcid'] = data['pcid']
        response_key['servertime'] = data['servertime']
        username=self.encode_username('504772813@qq.com')
        password = self.encode_password('543324797a.5', response_key['servertime'], response_key['nonce'],
                                        response_key['pubkey'])
        url='https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'+'&_=%s&openapilogin=qrcode' %get_time()
        yield scrapy.FormRequest(url,headers={
            'Accept':'*/*',
            'Connection':'keep-alive',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'login.sina.com.cn',
            'Origin':'https://api.weibo.com',
            'Referer':'https://api.weibo.com/oauth2/authorize?client_id=884965267&redirect_uri=https://id.amap.com/index/weibo?passport=1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        },formdata={
            'entry':'openapi',
            'gateway':'1',
            'from':'',
            'savestate':'0',
            'useticket':'1',
            'pagerefer':'',
            'ct':'1800',
            's':'1',
            'vsnf':'1',
            'vsnval':'',
            'door':'',
            'appkey':'1qkPGX',
            'su':username,
            'service':'miniblog',
            'servertime':str(response_key['servertime']),
            'nonce':str(response_key['nonce']),
            'pwencode':'rsa2',
            'rsakv':str(response_key['rsakv']),
            'sp':password,
            'sr':'1366*768',
            'encoding':'UTF-8',
            'cdult':'2',
            'domain':'weibo.com',
            'prelt':'88',
            'returntype':'TEXT',
        },dont_filter=True,callback=self.load_end,meta={"cookiejar": response.meta['cookiejar']})

    def load_end(self, response):
        data=json.loads(response.body.decode())
        url='https://api.weibo.com/oauth2/authorize'
        yield scrapy.FormRequest(url,headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'api.weibo.com',
            'Origin':'https://api.weibo.com',
            'Referer':'https://api.weibo.com/oauth2/authorize?client_id=884965267&redirect_uri=https://id.amap.com/index/weibo?passport=1',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        },formdata={
            'action':'login',
            'display':'default',
            'withOfficalFlag':'0',
            'quick_auth':'false',
            'withOfficalAccount':'',
            'scope':'',
            'ticket':data['ticket'],
            'isLoginSina':'',
            'response_type':'code',
            'regCallback':'https%3A%2F%2Fapi.weibo.com%2F2%2Foauth2%2Fauthorize%3Fclient_id%3D'+'884965267'+'%26response_type%3Dcode%26display%3Ddefault%26redirect_uri%3Dhttps%253A%252F%252Fid.amap.com%252Findex%252Fweibo%253Fpassport%253D1%26from%3D%26with_cookie%3D',
            'redirect_uri':'https://id.amap.com/index/weibo?passport=1',
            'client_id':'884965267',
            'appkey62':'1qkPGX',
            'state':'',
            'verifyToken':'null',
            'from':'',
            'switchLogin':'0',
            'userId':'',
            'passwd':'',
        },dont_filter=True,callback=self.load_authorize,meta={"cookiejar": response.meta['cookiejar']})

    def load_authorize(self,response):
        url=response.headers['Location'].decode()
        yield scrapy.Request(url,headers={
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.8',
            'cache-control':'max-age=0',
            'referer':'https://api.weibo.com/oauth2/authorize?client_id=884965267&redirect_uri=https://id.amap.com/index/weibo?passport=1',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        },dont_filter=True,callback=self.login_end,meta={"cookiejar": response.meta['cookiejar']})

    def login_end(self,response):
        db = web.database(dbn='mysql',db='pet_cloud',user='work',pw='phkAmwrF',port=3306,host='10.15.1.14')
        sql='''select count(*) from o2o.t_hh_dianping_shop_info where category2_name='综合商场';''' % brand
        temps = db.query(sql)
        print temps
        counts=counts[0]['count(*)']
        start_count=0
        for i in range(start_count,counts,10):
            sql="select * from o2o.t_hh_dianping_shop_info where category2_name='综合商场' limit %s,10; " %i
        	temps = db.query(sql)
            for v,temp in enumerate(temps):
                aoiid=temp['gaode_id']
                city=temp['city_name']
                if aoiid=='':
                    continue
                dt_format = time.strftime('%Y-%m-%d', time.localtime(time.time() - 3600 * 24))
                dt=re.sub('-','',dt_format)
                url='http://index.amap.com/service/aoi-index?aoiids=%s&end=%s&offset=30&byhour=0&refresh=0' %(aoiid,dt)
                yield scrapy.Request(url,headers={
                    'Accept':'application/json, text/javascript, */*; q=0.01',
                    'Referer':'http://index.amap.com/detail/%s?adcode=110000' %aoiid,
                    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
                    'X-Requested-With':'XMLHttpRequest',
                    },dont_filter=True,callback=self.test_data,
                                     meta={"cookiejar": response.meta['cookiejar'],
                                           'item':{'aoiid':aoiid,'city':city,'dt':dt_format,'i':i+v}})


    def test_data(self,response):
        item=MapStaticspeopleItem()
        org_data=json.loads(response.body.decode())
        aoiid=response.meta['item']['aoiid']
        if int(org_data['status'])==0:
            datas=org_data['data'][aoiid]
            # print(datas)
            for data in datas:
                count=data[3]
                day=data[0]
                day=time.mktime(time.strptime(day, '%Y%m%d'))
                day=time.strftime('%Y-%m-%d', time.localtime(day))
                item['city']=response.meta['item']['city']
                item['spot_id'] = response.meta['item']['aoiid']
                item['val'] = count
                item['dt'] = day
                yield item
        elif int(org_data['status'])==10:
            raise CloseSpider('Anti crawling')
    
    