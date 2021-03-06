# -*- encoding:utf-8 -*-
import sys

sys.path.append('../')
import web

from scrapy.exceptions import NotConfigured
from scrapy import signals
from twisted.internet import task

db = web.database(dbn='mysql', db='hillinsight', user='work', pw='phkAmwrF', port=3306, host='10.15.1.24')


def update_task_stats(t_uid, task_stats):
    try:
        db.update('t_platform_jobs', where="uid = '%s'" % t_uid, stats_dump='%s' % task_stats)
    except:
        pass


def update_task_performance(t_uid, perf):
    try:
        db.update('t_platform_jobs', where="uid = '%s'" % t_uid, spider_perf='%s' % perf)
    except:
        pass


def update_result_path(t_uid, result_path):
    try:
        db.update('t_platform_jobs', where="uid = '%s'" % t_uid, result_path='%s' % result_path)
    except:
        pass


def get_output_performance(engine, stats, spider):
    result = {}
    result['engine.slot.scheduler.mqs'] = len(engine.slot.scheduler.mqs)
    result['engine.downloader.active'] = len(engine.downloader.active)
    result['engine.scraper.slot.active'] = len(engine.scraper.slot.active)
    result['engine.scraper.slot.itemproc_size'] = engine.scraper.slot.itemproc_size
    result['item_scraped_count'] = stats.get_value('item_scraped_count') or 0
    result['engine.scraper.slot.active_size'] = engine.scraper.slot.active_size

    return result


def get_spider_stats(stats, spider, process):
    spider_stats = stats.get_stats()
    if 'close_spider' == process and spider_stats.has_key('finish_time') and spider_stats['finish_time']:
        spider_stats['start_time'] = spider_stats['start_time'].strftime("%Y-%m-%d %H:%M:%S")
        spider_stats['finish_time'] = spider_stats['finish_time'].strftime("%Y-%m-%d %H:%M:%S")
    # else:
    #     spider_stats['finish_time'] = '0001-01-01 01:01:01'
    spider.logger.info(spider_stats)
    return spider_stats


class PrintCoreMetrics(object):
    """
    An extension that prints "core metrics"
    """

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            crawler=crawler,
            task_uid=crawler.settings.get("TASK_UID", "tmp"),
            feed_uri=crawler.settings.get("FEED_URI", ""),
        )

    def __init__(self, crawler, task_uid, feed_uri):
        self.crawler = crawler
        self.interval = crawler.settings.getfloat('CORE_METRICS_INTERVAL', 5.0)
        self.task_uid = task_uid
        self.feed_uri = feed_uri

        if not self.interval:
            raise NotConfigured

        cs = crawler.signals
        cs.connect(self._spider_opened, signal=signals.spider_opened)
        cs.connect(self._spider_closed, signal=signals.spider_closed)

    def _spider_opened(self, spider):
        self.task = task.LoopingCall(self._log, spider)
        self.task.start(self.interval)

    def _spider_closed(self, spider, reason):
        stats = self.crawler.stats
        spider_stats = get_spider_stats(stats, spider, 'close_spider')
        update_task_stats(self.task_uid.strip(), spider_stats)
        spider.logger.info(reason)
        update_result_path(self.task_uid, self.feed_uri)

    def _log(self, spider):
        engine = self.crawler.engine
        stats = self.crawler.stats

        perf = get_output_performance(engine, stats, spider)
        update_task_performance(self.task_uid.strip(), perf)

        spider_stats = get_spider_stats(stats, spider, 'running')
        update_task_stats(self.task_uid.strip(),spider_stats)
