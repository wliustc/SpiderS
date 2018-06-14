# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from PIL import Image
import random
import logging
import web
import json
import traceback
import time
from io import BytesIO
import base64
import hashlib
import time
import urllib
import urllib2
import json
import os
import string

FATEA_PRED_URL  = "http://pred.fateadm.com"

def LOG(log):
    # 不需要测试时，注释掉日志就可以了
    # print(log);
    log = None;

class TmpObj():
    def __init__(self):
        self.init   = True;
        self.value  = None;

class Rsp():
    def __init__(self):
        self.ret_code   = -1;
        self.cust_val   = 0.0;
        self.err_msg    = "succ";
        self.pred_rsp   = TmpObj();

    def ParseJsonRsp(self, rsp_data):
        if rsp_data is None:
            self.err_msg = "http request failed, get rsp Nil data";
            return
        jrsp = json.loads( rsp_data);
        self.ret_code = int(jrsp["RetCode"]);
        self.err_msg = jrsp["ErrMsg"];
        self.request_id = jrsp["RequestId"];
        if self.ret_code == 0:
            rslt_data = jrsp["RspData"];
            if rslt_data is not None and rslt_data != "":
                jrsp_ext = json.loads( rslt_data);
                if "cust_val" in jrsp_ext:
                    data = jrsp_ext["cust_val"];
                    self.cust_val   = int(data);
                if "result" in jrsp_ext:
                    data        = jrsp_ext["result"];
                    self.pred_rsp.value     = data;

def CalcSign(usr_id, passwd, timestamp):
    md5     = hashlib.md5();
    md5.update((timestamp + passwd).encode("utf-8"));
    csign   = md5.hexdigest();

    md5     = hashlib.md5();
    md5.update((usr_id + timestamp + csign).encode("utf-8"));
    csign   = md5.hexdigest();
    return csign;

def CalcCardSign(cardid, cardkey, timestamp, passwd):
    md5     = hashlib.md5();
    md5.update(passwd + timestamp + cardid + cardkey);
    return md5.hexdigest();

def HttpRequest(url, body_data):
    rsp         = Rsp()
    post_data   = urllib.urlencode(body_data);
    # request     = urllib.request.urlopen(url, post_data.encode('utf8'))
    request = urllib2.Request(url, post_data.encode('utf8'))
    request.add_header( "User-Agent", "Mozilla/5.0");
    rsp_data    = urllib2.urlopen(request ).read();
    rsp.ParseJsonRsp( rsp_data);
    return rsp;

class FateadmApi():
    def __init__(self, app_id, app_key, usr_id, usr_key):
        self.app_id     = app_id;
        if app_id is None:
            self.app_id = "";
        self.app_key    = app_key;
        self.usr_id     = usr_id;
        self.usr_key    = usr_key;
        self.host       = FATEA_PRED_URL;

    def SetHost(self, url):
        self.host       = url;
    #
    # 查询余额
    #
    def QueryBalc(self):
        tm      = str( int(time.time()));
        sign    = CalcSign( self.usr_id, self.usr_key, tm);
        param   = {
                "user_id": self.usr_id,
                "timestamp":tm,
                "sign":sign
                };
        url     = self.host + "/api/custval"
        rsp     = HttpRequest(url, param);
        if rsp.ret_code == 0:
            LOG("query succ ret: {} cust_val: {} rsp: {} pred: {}".format( rsp.ret_code, rsp.cust_val, rsp.err_msg, rsp.pred_rsp.value));
        else:
            LOG("query failed ret: {} err: {}".format( rsp.ret_code, rsp.err_msg.encode('utf-8')));
        return rsp;

    #
    # 查询网络延迟
    #
    def QueryTTS(self, pred_type):
        tm          = str( int(time.time()));
        sign        = CalcSign( self.usr_id, self.usr_key, tm);
        param       = {
                "user_id": self.usr_id,
                "timestamp":tm,
                "sign":sign,
                "predict_type":pred_type,
                }
        if self.app_id != "":
            #
            asign       = CalcSign(self.app_id, self.app_key, tm);
            param["appid"]     = self.app_id;
            param["asign"]      = asign;
        url     = self.host + "/api/qcrtt";
        rsp     = HttpRequest(url, param);
        if rsp.ret_code == 0:
            LOG("query rtt succ ret: {} request_id: {} err: {}".format( rsp.ret_code, rsp.request_id, rsp.err_msg));
        else:
            LOG("predict failed ret: {} err: {}".format( rsp.ret_code, rsp.err_msg.encode('utf-8')));
        return rsp;

    #
    # 识别验证码
    #
    def Predict(self, pred_type, img_data):
        tm          = str( int(time.time()));
        sign        = CalcSign( self.usr_id, self.usr_key, tm);
        img_base64  = base64.b64encode( img_data);
        param       = {
                "user_id": self.usr_id,
                "timestamp":tm,
                "sign":sign,
                "predict_type":pred_type,
                "img_data":img_base64,
                }
        if self.app_id != "":
            #
            asign       = CalcSign(self.app_id, self.app_key, tm);
            param["appid"]     = self.app_id;
            param["asign"]      = asign;
        url     = self.host + "/api/capreg";
        rsp     = HttpRequest(url, param);
        if rsp.ret_code == 0:
            LOG("predict succ ret: {} request_id: {} pred: {} err: {}".format( rsp.ret_code, rsp.request_id, rsp.pred_rsp.value, rsp.err_msg));
        else:
            LOG("predict failed ret: {} err: {}".format( rsp.ret_code, rsp.err_msg.encode('utf-8')));
            if rsp.ret_code == 4003:
                #lack of money
                LOG("cust_val <= 0 lack of money, please charge immediately");
        return rsp

    #
    # 从文件进行验证码识别
    #
    def PredictFromFile( self, pred_type, file_name=None,data=None):
        if file_name:
            with open(file_name, "rb+") as f:
                data = f.read()
        elif not file_name and not data:
            raise TypeError('file_name or data should give one')
        return self.Predict( pred_type, data)

    #
    # 识别失败，进行退款请求
    # 注意:
    #    Predict识别接口，仅在ret_code == 0时才会进行扣款，才需要进行退款请求，否则无需进行退款操作
    # 注意2:
    #   退款仅在正常识别出结果后，无法通过网站验证的情况，请勿非法或者滥用，否则可能进行封号处理
    #
    def Justice(self, request_id):
        if request_id == "":
            #
            return ;
        tm          = str( int(time.time()));
        sign        = CalcSign( self.usr_id, self.usr_key, tm);
        param       = {
                "user_id": self.usr_id,
                "timestamp":tm,
                "sign":sign,
                "request_id":request_id
                }
        url     = self.host + "/api/capjust";
        rsp     = HttpRequest(url, param);
        if rsp.ret_code == 0:
            LOG("justice succ ret: {} request_id: {} pred: {} err: {}".format( rsp.ret_code, rsp.request_id, rsp.pred_rsp.value, rsp.err_msg));
        else:
            LOG("justice failed ret: {} err: {}".format( rsp.ret_code, rsp.err_msg.encode('utf-8')));
        return rsp;

    #
    # 充值接口
    #
    def Charge(self, cardid, cardkey):
        tm          = str( int(time.time()));
        sign        = CalcSign( self.usr_id, self.usr_key, tm);
        csign       = CalcCardSign(cardid, cardkey, tm, self.usr_key);
        param       = {
                "user_id": self.usr_id,
                "timestamp":tm,
                "sign":sign,
                'cardid':cardid,
                'csign':csign
                }
        url = self.host + "/api/charge";
        rsp = HttpRequest(url, param);
        if rsp.ret_code == 0:
            LOG("charge succ ret: {} request_id: {} pred: {} err: {}".format( rsp.ret_code, rsp.request_id, rsp.pred_rsp.value, rsp.err_msg));
        else:
            LOG("charge failed ret: {} err: {}".format( rsp.ret_code, rsp.err_msg.encode('utf-8')));
        return rsp


uaList = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
]

class LoginScrapySpider(scrapy.Spider):
    name = "login_scrapy"
    allowed_domains = ["sz.jd.com"]
    start_urls = ['http://sz.jd.com/']


    def login_(self,user, pawd, tt):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (random.choice(uaList))
        driver = webdriver.PhantomJS()
        # driver=webdriver.Chrome(r'D:\gongju\chromedriver.exe ')
        # driver.set_window_size(1920, 1080)
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)  # 这两种设置都进行才有效
        try:
            driver.get('https://sz.jd.com/index.html')
            # 点击登录按钮
            wait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div'))).click()
            # 切换Iframe
            time.sleep(5)
            iframe_button = wait(driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="ui-dialog-content"]/iframe')))
            left = iframe_button.location['x']
            top = iframe_button.location['y']
            elementWidth = iframe_button.location['x'] + iframe_button.size['width']
            elementHeight = iframe_button.location['y'] + iframe_button.size['height']
            driver.switch_to.frame(iframe_button)
            time.sleep(5)
            # 登录按钮
            account_button = wait(driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="login-tab login-tab-r"]')))
            account_button.click()
            time.sleep(5)

            # 用户名输入框
            account_input = wait(driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="loginname"]')))
            account_input.send_keys(user)
            # 密码输入框
            passwd_input = wait(driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="nloginpwd"]')))
            passwd_input.send_keys(pawd)
            # 登录确定按钮
            submit_button = driver.find_element_by_xpath('//div[@class="login-btn"]/a[@id="loginsubmit"]')
            submit_button.click()
            time.sleep(5)
            try:
                temp=driver.find_element_by_xpath("//img[@id='JD_Verification1']")
            except Exception as e:
                temp=None
            if temp:
                temp.click()
                time.sleep(5)
                for i in range(1, 3):
                    all_page=driver.get_screenshot_as_png()
                    left_baidu = temp.location['x']+12
                    top_baidu = temp.location['y'] + 47
                    elementWidth_baidu = temp.size['width'] + left_baidu
                    elementHeight_baidu = temp.size['height'] + top_baidu
                    print(left_baidu,top_baidu,elementWidth_baidu,elementHeight_baidu)
                    picture = Image.open(BytesIO(all_page))
                    picture = picture.crop((left_baidu, top_baidu, elementWidth_baidu, elementHeight_baidu))
                    imgByteArr = BytesIO()
                    picture.save(imgByteArr, format='PNG')
                    imgByteArr = imgByteArr.getvalue()
                   # with open('2_%s.png' %i,'wb') as f:
                    #    f.write(imgByteArr)
                    rsp = self.api.PredictFromFile(self.pred_type,data=imgByteArr)   #上传到服务器
                    #rsp=Rsp()
                    #rsp.ret_code=0
                    #tmp = driver.find_element_by_xpath("//img[@id='JD_Verification1']")    #验证码错误
                    if rsp.ret_code == 0:
                        verification = wait(driver, 500).until(
                            EC.presence_of_element_located((By.XPATH, '//input[@id="authcode"]')))
                        print('**********验证码为:%s******验证次数为:%s**************' %(rsp.pred_rsp.value,i))
                        verification.send_keys(rsp.pred_rsp.value)  # (rsp.pred_rsp.value)
                        time.sleep(1)
              #          driver.get_screenshot_as_file('1_%s.png' %i)
                        submit_button.click()
                        time.sleep(5)
                        try:
                            tmp = driver.find_element_by_xpath("//img[@id='JD_Verification1']")    #验证码错误
                            #self.api.Justice(resp.request_id)
                            print('验证码错误')
                            if i==3:
                                driver.close()
                                driver.quit()
                                return None
                            	#验证不成功
                        except Exception as e:
                            break
                    else:
                        driver.close()
                        driver.quit()
                        return None     #可能无法获取打码平台服务
            # 退出Ifraame
            time.sleep(10)

            # 获取cookie
            cooke_dict = driver.get_cookies()

            # 字典化cookie
            result = {}
            for i in cooke_dict:
                result[i["name"]] = i["value"]
            # 关闭webdriver
            driver.close()
            driver.quit()
            if 'pin' in result:
                return result
            else:
                tt -= 1
                if tt > 0:
                    users = user
                    pwad = pawd
                    self.login_(users, pwad, tt)
        except:
            traceback.print_exc()
            driver.close()
            driver.quit()
            tt -= 1
            if tt > 0:
                users = user
                pwad = pawd
                self.login_(users, pwad, tt)

    def start_requests(self):
        usr_id = "102200"
        usr_key = "71hqHGLUgomkRkedd763iqPuRTHPsPKi"
        app_id = "302402"
        app_key = "yMlJAPMH2DVurjDgDkhH6VF3KxXBJHHa"
        self.pred_type = "30400"
        self.api=FateadmApi(app_id, app_key, usr_id, usr_key)
        db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
        sql = '''select user,pawd,name from t_spider_JD_shangzhi where name not in(
	select shop_name from hillinsight.t_spiedr_JD_cookies where `dt`=date(now())
);'''
        for i in db.query(sql):
            user = i.get('user')
            pawd = i.get('pawd')
            shop_name = i.get('name')
            yield scrapy.Request('https://sz.jd.com/index.html',meta={'noneeedrequest':1,'user':user,
                                    'pawd':pawd,'shop_name':shop_name},dont_filter=True)
    def parse(self, response):
        user = response.meta['user']
        pawd = response.meta['pawd']
        shop_name = response.meta['shop_name']
        cookies = json.dumps(self.login_(user, pawd, 5))
        dt=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if not cookies or 'wlfstk_smdl' not in cookies or cookies=='null':
            if 'retry_time' not in response.meta:
                retry_time=1
            else:
                retry_time=response.meta['retry_time']
            if retry_time<3:
                retry_time+=1
                yield response.request
            else:
                return
        db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
        if not cookies=='null':
            sql = '''replace into t_spiedr_JD_cookies(shop_name,cookies,dt)  VALUES ("{}",'{}',"{}"); '''.format(shop_name, cookies,dt)
            db.query(sql)
            item={'shop_name':shop_name,'cookies':cookies}
            yield item

    
    
    
    
    