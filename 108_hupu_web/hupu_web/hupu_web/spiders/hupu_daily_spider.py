# -*- coding: utf-8 -*-
import scrapy
import re
from hupu_web.items import HupuWebItem
import time
import datetime
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/54.0.2840.98 Safari/537.36"}


class Hupu_Spider(scrapy.Spider):

    name = 'hupu_daily_spider'
    allowed_domains = 'hupu.com'

    def start_requests(self):
        url = 'https://bbs.hupu.com/boards.php'

        yield scrapy.Request(url, headers=headers, callback=self.classify_parse, dont_filter=True)

    def classify_parse(self, response):
        content = response.body
        pattern = re.compile('"plate_03([\s\S]*?)</li></ul>')
        con_list = re.findall(pattern, content)
        for con in con_list:
            pattern1 = re.search('<h3>(.*?)</h3>', con)
            board_classify = pattern1.group(1)
            pattern2 = re.compile('<a href="(.*?)" target="_blank">(.*?)<')
            board_list = re.findall(pattern2, con)
            for board in board_list:
                page = 1
                board_url = 'https://bbs.hupu.com' + board[0] + '-' + str(page)
                board_name = board[1]

                yield scrapy.Request(board_url, headers=headers, callback=self.boards_parse,
                                     meta={'board_classify': board_classify, 'board_name': board_name, 'page': page,
                                           'href': board[0]},
                                     dont_filter=True)

    def boards_parse(self, response):
        content = response.body
        board_classify = response.meta['board_classify']
        board_name = response.meta['board_name']
        page = response.meta['page']
        href = response.meta['href']
        items = HupuWebItem()
        pattern = re.compile('<td id="" class="p_title">([\s\S]*?)</tr>')
        con_list = re.findall(pattern, content)
        if con_list and page <= 30:
            page += 1
            for con in con_list:
                pattern1 = re.compile('class=\"p_re\">(\d+) / (\d+)<')
                num_data = re.findall(pattern1, con)[0]
                reply_num = num_data[0]
                browse_num = num_data[1]
                pattern2 = re.compile('<a id="" href="(.*?)\.html">([\s\S]*?)</a>')
                posts_data = re.findall(pattern2, con)[0]
                page_num = 1
                posts_href = posts_data[0]
                posts_url = 'https://bbs.hupu.com' + posts_href + '-' + str(page_num) + '.html'
                posts_title = re.sub('<.*?>', '', posts_data[1])
                if reply_num != '0':
                    pattern3 = re.compile('"查看最后回复">(.*?)</a>')
                    date = re.findall(pattern3, con)[0]
                    now = datetime.datetime.now()
                    before = now - datetime.timedelta(days=1)
                    yes_date = before.strftime('%m-%d')
                    if date == yes_date:
                        mobile_num = 0
                        yield scrapy.Request(posts_url, headers=headers, callback=self.posts_parse,
                                             meta={'board_classify': board_classify, 'board_name': board_name,
                                                   'posts_href': posts_href, 'page_num': page_num,
                                                   'mobile_num': mobile_num, 'date': date,
                                                   'browse_num': browse_num, 'posts_title': posts_title},
                                             dont_filter=True)
                else:
                    pattern3 = re.compile('"查看最后回复">(.*?)</a>')
                    date = re.findall(pattern3, con)[0]
                    now = datetime.datetime.now()
                    before = now - datetime.timedelta(days=1)
                    yes_date = before.strftime('%m-%d')
                    if date == yes_date:
                        items['board_classify'] = board_classify
                        items['board_name'] = board_name
                        items['browse_num'] = browse_num
                        items['posts_title'] = posts_title
                        items['from_mobile_reply_num'] = '0'
                        items['post_id'] = re.findall('\d+', posts_href)[0]
                        items['last_reply_date'] = '2017-' + date
                        yield items

            board_url = 'https://bbs.hupu.com' + href + '-' + str(page)
            yield scrapy.Request(board_url, headers=headers, callback=self.boards_parse,
                                 meta={'board_classify': board_classify, 'board_name': board_name, 'page': page,
                                       'href': href},
                                 dont_filter=True)

    def posts_parse(self, response):
        content = response.body
        board_classify = response.meta['board_classify']
        board_name = response.meta['board_name']
        browse_num = response.meta['browse_num']
        posts_title = response.meta['posts_title']
        mobile_num = response.meta['mobile_num']
        date = response.meta['date']
        posts_href = response.meta['posts_href']
        page_num = response.meta['page_num']
        items = HupuWebItem()
        pattern = re.compile('发自虎扑体育(.*?)客户端')
        print response.meta['proxy']
        mobile_num = len(re.findall(pattern, content)) + mobile_num
        if '下一页' in content:
            page_num += 1
            posts_url = 'https://bbs.hupu.com' + posts_href + '-' + str(page_num) + '.html'
            yield scrapy.Request(posts_url, headers=headers, callback=self.posts_parse,
                                 meta={'board_classify': board_classify, 'board_name': board_name,
                                       'posts_href': posts_href, 'page_num': page_num, 'mobile_num': mobile_num,
                                       'browse_num': browse_num, 'posts_title': posts_title, 'date': date},
                                 dont_filter=True)
        else:
            items['board_classify'] = board_classify
            items['board_name'] = board_name
            items['browse_num'] = browse_num
            items['posts_title'] = re.sub('\n', '', posts_title)
            items['from_mobile_reply_num'] = mobile_num
            items['last_reply_date'] = date
            items['post_id'] = re.findall('\d+', posts_href)[0]
            items['last_reply_date'] = '2017-' + date
            yield items
