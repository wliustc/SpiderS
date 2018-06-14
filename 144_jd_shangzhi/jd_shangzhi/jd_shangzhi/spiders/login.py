# -*- coding: utf-8 -*-
import scrapy

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import time
import random
import web
import json
import traceback
import time
uaList = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    'Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
]
class LoginSpider(scrapy.Spider):
    name = "login"
    allowed_domains = ["sz.jd.com"]
    def login_(self,user, pawd, tt):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (random.choice(uaList))
        driver = webdriver.PhantomJS()
        # driver=webdriver.Chrome(r'D:\gongju\chromedriver.exe ')
        driver.set_window_size(1920, 1080)
        driver.set_page_load_timeout(30)
        driver.set_script_timeout(30)  # 这两种设置都进行才有效
        try:
            driver.get('https://sz.jd.com/index.html')
            # 点击登录按钮
            wait(driver, 200).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div'))).click()
            # 切换Iframe
            iframe_button = wait(driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="ui-dialog-content"]/iframe')))
            driver.switch_to.frame(iframe_button)
            time.sleep(5)
            # 登录按钮
            account_button = wait(driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="login-tab login-tab-r"]')))
            account_button.click()
            time.sleep(5)

            # 用户名输入框
            # account_input = driver.find_element_by_xpath('//input[@id="loginname"]')
            account_input = wait(driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="loginname"]')))
            # account_input.send_keys(u'CAT-商智')
            account_input.send_keys(user)
            # 密码输入框
            # passwd_input = driver.find_element_by_xpath('//input[@id="nloginpwd"]')
            passwd_input = wait(driver, 500).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="nloginpwd"]')))
            # passwd_input.send_keys(u'cat123789')
            passwd_input.send_keys(pawd)
            # 登录确定按钮
            submit_button = driver.find_element_by_xpath('//div[@class="login-btn"]/a[@id="loginsubmit"]')
            submit_button.click()

            # 退出Ifraame
            driver.switch_to_default_content()
            time.sleep(10)

            # 获取cookie
            cooke_dict = driver.get_cookies()

            # 字典化cookie
            result = {}
            for i in cooke_dict:
                result[i["name"]] = i["value"]
            driver.get_screenshot_as_file("login.png")
            # 关闭webdriver
            driver.close()
            driver.quit()
            # return result
            if 'pin' in result:
                # print('******************************')
                # print(result)
                # print('******************************')
                return result
            else:
                tt -= 1
                if tt > 0:
                    users = user
                    pwad = pawd
                    self.login_(users, pwad, tt)
        except:
            self.logger.error(traceback.print_exc())
            driver.close()
            driver.quit()
            tt -= 1
            if tt > 0:
                users = user
                pwad = pawd
                self.login_(users, pwad, tt)

    def start_requests(self):
        db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
        sql = '''select user,pawd,name from t_spider_JD_shangzhi;'''
        for i in db.query(sql):
            user = i.get('user')
            pawd = i.get('pawd')
            shop_name = i.get('name')
            yield scrapy.Request('https://sz.jd.com/index.html',meta={'noneeedrequest':1,'user':user,
                                    'pawd':pawd,'shop_name':shop_name},dont_filter=True)
    def parse(self, response):
        db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
        user = response.meta['user']
        pawd = response.meta['pawd']
        shop_name = response.meta['shop_name']
        cookies = json.dumps(self.login_(user, pawd, 5))
        dt=time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if not cookies or 'wlfstk_smdl' not in cookies:
            if 'retry_time' not in response.meta:
                retry_time=1
            else:
                retry_time=response.meta['retry_time']
            if retry_time<3:
                retry_time+=1
                yield response.request

        sql = '''replace into t_spiedr_JD_cookies(shop_name,cookies,dt)  VALUES ("{}",'{}',"{}"); '''.format(shop_name, cookies,dt)
        db.query(sql)
        item={'shop_name':shop_name,'cookies':cookies}
        yield item
    
    
    
    