# -*- coding: utf-8 -*-
import scrapy
import re
from fang.items import FangDetailItem
from scrapy.selector import Selector
import web
import urlparse
# from utils.gps_coords_convertor import GPSCoordsConvertor
import json
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (compatible; Baiduspider-render/2.0;+http://www.baidu.com/search/spider.html)",
    "referer": 'https://www.baidu.com'
}
db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
db2 = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')


class fang_detail_spider(scrapy.Spider):

    name = 'fang_detail_spider'

    def start_requests(self):
        sql = '''
               select csi_id, link, src_uid, city
               from t_hh_community_source_info
               where frm='搜房'  and src_uid REGEXP '^[0-9]*$' AND households=0 AND property_type NOT LIKE '%写字楼%' AND property_type NOT LIKE '%商铺%'
              '''
        results = db.query(sql)
        for data in results:
            csi_id = data['csi_id']
            url = data['link']
            src_uid = data['src_uid']
            city = data['city']
            yield scrapy.Request(url, headers=headers, callback=self.argparse, meta={'csi_id': csi_id, 'link': url,
                                                                                     'src_uid': src_uid, 'city': city},
                                 dont_filter=True)

    def argparse(self, response):
        content = response.body.decode('gb18030').encode('utf8')
        csi_id = response.meta['csi_id']
        # link = response.meta['link']
        src_uid = response.meta['src_uid']
        city = response.meta['city']
        hxs = Selector(text=content)
        url_prefix = response.url
        newcode = ''
        if response.url.startswith('http://fangjia.fang.com'):
            newcode = src_uid
            pattern1 = re.search('class="more-detail" href="(.*?)"', content)
            url_prefix = pattern1.group(1)
        else:
            newcode_sec = hxs.xpath('//meta[@name="mobile-agent"]/@content').extract()
            if newcode_sec:
                newcode_re = re.search('.*/(\d+)\..*', newcode_sec[0])
                if newcode_re:
                    newcode = newcode_re.group(1)
            else:
                newcode_sec = hxs.xpath('//div[@class="blmapbox"]/iframe/@src').extract()
                if newcode_sec:
                    newcode_re = re.search('.*newcode=(\d+).*', newcode_sec[0])
                    if newcode_re:
                        newcode = newcode_re.group(1)
        if url_prefix.endswith('htm') or url_prefix.endswith('html') or url_prefix.endswith('php'):
            sql = '''
                    select link from t_hh_community_source_info
                    WHERE frm='搜房' AND city='%s' and link LIKE 'http://%%fang.com/'
                    limit 1
                  ''' % (city)
            res = db.query(sql)
            if res:
                url_prefix = res[0]['link']
        url_parts = urlparse.urlparse(url_prefix)
        api_url = "%s://%s/house/ajaxrequest/dongpic.php" % (url_parts.scheme, url_parts.netloc)
        post_data = {'newcode': newcode, 'loudongIds': 'false'}
        header2 = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.110 Safari/537.36',
            'referer': response.url
        }

        yield scrapy.FormRequest(api_url, formdata=post_data, headers=header2, callback=self.jsonparse, dont_filter=True,
                                 meta={'csi_id': csi_id})

    def jsonparse(self, response):
        json_data = json.loads(response.body)
        csi_id = response.meta['csi_id']
        items = FangDetailItem()
        proj_info = None
        if 'proj_info' in json_data:
            proj_info = json_data['proj_info']
            # (lng, lat) = GPSCoordsConvertor.baidu_coord_2_gps(float(proj_info['coord_x']),
            #                                               float(proj_info['coord_y']))
        if proj_info:
            items['csi_id'] = csi_id
            items['district'] = proj_info['District']
            items['position'] = proj_info['ComArea']
            items['address'] = proj_info['Address']
            items['longitude'] = proj_info['coord_x']
            items['latitude'] = proj_info['coord_y']
            items['built_dt'] = proj_info['FinishDate']
            items['developer'] = proj_info['Developer']
            items['property_company'] = proj_info['PropertyManage']
            items['property_type'] = proj_info['proj_type']
            items['property_fee'] = 0 if not proj_info['PropertyFee'] else proj_info['PropertyFee']
            items['covered_area'] = proj_info['PurposeArea']
            items['households'] = proj_info['TotalDoor']
            items['cur_households'] = proj_info['PartTotalDoor']
            items['plot_ratio'] = proj_info['Dimension']
            items['greening_rate'] = float(proj_info['VirescenceRate']) / 100

            # key_str = ','.join('`%s`' % k for k in items.keys())
            # value_str = ','.join(
            #     'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v) for v in
            #     items.values())
            # kv_str = ','.join(
            #     "`%s`=%s" % (k, 'NULL' if v is None or v == 'NULL' else "'%s'" % MySQLdb.escape_string('%s' % v))
            #     for (k, v)
            #     in items.items())
            # sql = "INSERT INTO t_hh_community_source_info(%s) VALUES(%s)" % (key_str, value_str)
            # sql = "%s ON DUPLICATE KEY UPDATE %s" % (sql, kv_str)
            # db.query(sql)
            yield items