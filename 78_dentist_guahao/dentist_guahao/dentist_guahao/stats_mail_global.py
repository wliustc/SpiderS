# -*- encoding:utf-8 -*-
"""
StatsMailer extension sends an email when a spider finishes scraping.

Use STATSMAILER_RCPTS setting to enable and give the recipient mail address
"""

from scrapy import signals
from scrapy.mail import MailSender
from scrapy.exceptions import NotConfigured
from collections import OrderedDict

import web
import json

web.config.debug = False
db = web.database(dbn='mysql', db='hillinsight', user='work', pw='phkAmwrF', port=3306, host='10.15.1.24')


def warn_condition(pre, cur):
    if pre > cur and abs(1.0 * (cur - pre)) / pre > 0.2:
        return True
    else:
        return False


def get_compare_result(cur_item_num, tid, uid):
    c_result = ''
    sql = '''SELECT stats_dump from t_platform_jobs where tid=%s and done_type=1 and uid!='%s' and  stats_dump is not NULL ORDER BY id desc limit 1;''' %(tid, uid)
    data = db.query(sql)
    if data and len(data) == 1:
        try:
            pre = json.loads(data[0]['stats_dump'].replace("'", '"'))
            if int(cur_item_num) == 0:
                return "Falied scraped None", c_result
            if int(pre['item_scraped_count']) == 0:
                compare_rate = "--"
            else:
                compare_rate = round((float(cur_item_num - pre['item_scraped_count'])/pre['item_scraped_count'])*100,2)
                compare_rate = str(compare_rate) + "%"
            url = "http://spider.in.hillinsight.com/manager/job/job_detail/%s"%uid
            c_result = '''<tr><th>上次抓取item的数量</th>\n <td>%s</td></tr>\n
                          <tr><th>抓取item数量环比</th>\n<td>%s</td></tr>\n
                          <tr><th>任务详情</th>\n<td><a href="%s">点击查看</a></td></tr>\n
                       ''' % (pre['item_scraped_count'], compare_rate, url)
            if warn_condition(pre['item_scraped_count'], cur_item_num):
                return "Warning items reduce", c_result
            else:
                return "Success", c_result
        except:
            pass
    return "Failed", c_result


def get_stats_content(stats):
    stats_content = ''
    need_items = {"start_time":"开始时间", "finish_time":"结束时间", "downloader/request_count":"总请求数",
                  "item_scraped_count":"抓取item的数量"}
    item_keys = need_items.keys()
    #sort_items = sorted(stats.items())
    for i in stats:
        if i in item_keys:
            stats_content += "<tr><th>%s</th>\n<td>%s</td></tr>\n" % (need_items[i], stats[i])
    return stats_content


class StatsMailer(object):
    def __init__(self, stats, recipients, mail, task_id, uid):
        self.stats = stats
        self.recipients = recipients
        self.mail = mail
        self.task_id = task_id
        self.uid = uid

    @classmethod
    def from_crawler(cls, crawler):
        recipients = crawler.settings.getlist("STATSMAILER_RCPTS")
        task_id = crawler.settings.get("TASK_ID", "")
        uid = crawler.settings.get("TASK_UID", "")
        if not recipients:
            raise NotConfigured
        mail = MailSender.from_settings(crawler.settings)
        o = cls(crawler.stats, recipients, mail, task_id, uid)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self, spider):
        spider_stats = self.stats.get_stats(spider)
        st_content = get_stats_content(spider_stats)
        cmp_st, com_result = get_compare_result(spider_stats['item_scraped_count'], self.task_id, self.uid)
        print "**con_result:%s"%com_result
        css_content = '''
        <style type="text/css">
            *{
                margin: 0;
                padding: 0;
            }
            body{
                font: italic 10px Georgia, serif;
                letter-spacing: normal;
                background-color: #f0f0f0;
            }
            #table1{
                font: bold 16px/1.4em "行书", sans-serif;
            }
            #table1 thead th{
                padding: 15px;
                border: 1px solid #93CE37;
                border-bottom: 3px solid #9ED929;
                text-shadow: 1px 1px 1px #568F23;
                color: #fff;
                background-color: #9DD929;
                border-radius: 5px 5px 0px 0px;
            }
            #table1 thead th:empty{
                background-color: transparent;
                border: none;
            }
            #table1 tbody th{
                padding: 0px 10px;
                border: 1px solid #93CE37;
                border-right: 3px solid #9ED929;
                text-shadow: 1px 1px 1px #568F23;
                color: #666;
                background-color: #9DD929;
                border-radius: 5px 0px 0px 5px;
            }
            #table1 tbody td{
                padding: 10px;
                border: 2px solid #E7EFE0;
                text-align: center;
                text-shadow: 1px 1px 1px #fff;
                color: #666;
                background-color: #DEF3CA;
                border-radius: 2px;
            }
        </style>'''
        mail_content = """
        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8"/>
            {css_content}
        </head>
        <body>
        <div>
            <table id="table1">
            <tbody>
                <tr>
                    <th>任务名称</th>
                    <td>{spider_name}</td>
                </tr>
                {stats_content}
                {compare_content}
            </tbody>
            </table>
        </div>
        </body>
        </html>
        """.format(spider_name=spider.name, css_content=css_content, stats_content=st_content, compare_content=com_result)
        mail_sub = "【%s】 Scrapy stats for: %s" % (cmp_st, spider.name)
        print "email-content:%s"%mail_content
        # body = "Global stats\n\n"
        # body += "\n".join("%-50s : %s" % i for i in self.stats.get_stats().items())
        # body += "\n\n%s stats\n\n" % spider.name
        # body += "\n".join("%-50s : %s" % i for i in spider_stats.items())
        return self.mail.send(self.recipients, mail_sub, mail_content, mimetype='text/html')
