import random
import time
import web
import redis
import json

db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
dt = 0


class ProxyMiddleware(object):

    def __init__(self):
        self.proxys = ''
        self.dt = 0

    def process_request(self, request, spider):
        if not self.proxys:
            self.proxys = self.redis_conn1()
        if self.proxys:
            proxy = random.choice(self.proxys)
            # if not divmod(int(time.time()), 5)[1]:
            if int(time.time()) - self.dt > 5:
                self.dt = int(time.time())
                self.proxys = self.redis_conn1()
            request.meta['proxy'] = "%s" % proxy
            print '-----------%s------------' % proxy
            request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'


    def redis_conn1(self):
        while True:
            try:
                r = redis.Redis(host='116.196.71.111', port=52385, db=0)
                data = r.smembers('proxy_data5u')
                if data:
                    proxy_res = []
                    for d in data:
                        dd = json.loads(d)
                        proxy_res.append('http://' + str(dd['ip']))
                    return proxy_res
            except:
                return []

