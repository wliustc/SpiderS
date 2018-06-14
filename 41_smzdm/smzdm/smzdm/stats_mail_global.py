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
    if pre > cur and 1.0 * (pre - cur) / 100 > 0.2:
        return True
    else:
        return False


def get_compare_result(tid):
    c_result = ''
    sql = 'SELECT stats_dump from t_platform_jobs where tid=%s and stats_dump is not NULL ORDER BY id desc limit 2;' % tid
    data = db.query(sql)
    if data and len(data) == 2:
        try:
            cur = json.loads(dict(data[0])['stats_dump'].replace("'", '"'))
            pre = json.loads(dict(data[1])['stats_dump'].replace("'", '"'))
            c_result = '<tr><td>items of this time: %s</td>\n <td>items of last time: %s</td></tr>\n' % (
                cur['item_scraped_count'], pre['item_scraped_count'])
            if warn_condition(pre['item_scraped_count'], cur['item_scraped_count']):
                return "Warning items reduce", c_result
            else:
                return "Success", c_result
        except:
            pass
    return "Success", c_result


def get_stats_content(stats):
    stats_content = ''
    sort_items = sorted(stats.items())
    for i in sort_items:
        stats_content += "<tr><td>%s</td>\n<td>%s</td></tr>\n" % i
    return stats_content


class StatsMailer(object):
    def __init__(self, stats, recipients, mail, task_id):
        self.stats = stats
        self.recipients = recipients
        self.mail = mail
        self.task_id = task_id

    @classmethod
    def from_crawler(cls, crawler):
        recipients = crawler.settings.getlist("STATSMAILER_RCPTS")
        task_id = crawler.settings.get("TASK_ID", "")
        if not recipients:
            raise NotConfigured
        mail = MailSender.from_settings(crawler.settings)
        o = cls(crawler.stats, recipients, mail, task_id)
        crawler.signals.connect(o.spider_closed, signal=signals.spider_closed)
        return o

    def spider_closed(self, spider):
        spider_stats = self.stats.get_stats(spider)
        st_content = get_stats_content(spider_stats)
        cmp_st, com_result = get_compare_result(self.task_id)
        mail_content = """
        <!doctype html>
        <html>
        <head><meta charset="utf-8"/></head>
        <body>
        <div style="">
            <table width="600" cellpadding="0" cellspacing="0" border="1" style="margin:0 auto;">
            <tbody>
                <tr>
                    <td>
                        <div style="width:600px;text-align:left;font:12px/15px simsun;color:#000;background:#fff;">
                            {spider_name} stats
                        </div>
                    </td>
                </tr>

                {stats_content}

                <tr>
                    <td>
                        <div style="width:600px;text-align:left;font:12px/15px simsun;color:#000;background:#fff;">
                            与上次结果对比
                        </div>
                    </td>
                </tr>

                {compare_content}

            </tbody>
            </table>
        </div>
        </body>
        </html>
        """.format(spider_name=spider.name, stats_content=st_content, compare_content=com_result)
        mail_sub = "【%s】 Scrapy stats for: %s" % (cmp_st, spider.name)
        # body = "Global stats\n\n"
        # body += "\n".join("%-50s : %s" % i for i in self.stats.get_stats().items())
        # body += "\n\n%s stats\n\n" % spider.name
        # body += "\n".join("%-50s : %s" % i for i in spider_stats.items())
        return self.mail.send(self.recipients, mail_sub, mail_content, mimetype='text/html')
