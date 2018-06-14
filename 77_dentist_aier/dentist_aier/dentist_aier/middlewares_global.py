import random
import base64
import web
db = web.database(dbn='mysql', db='hillinsight', user='work', pw='phkAmwrF', port=3306, host='10.15.1.24')
    
class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def __init__(self, agents):
        self.agents = agents
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
    def process_request(self, request, spider):
    #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))
class ProxyMiddleware(object):
    def __init__(self):
        self.proxys = ''
    def process_request(self, request, spider):
        if not self.proxys:
            self.proxys = self._get_proxy(spider)
        if self.proxys:
            proxy = random.choice(self.proxys)
            if  random.random() < 0.0001:
                self.proxys = self._get_proxy(spider)
            request.meta['proxy'] = "%s" % proxy
        print "******request:%s"%request.meta['proxy']
    def _get_proxy(self,spider):
        domain = getattr(spider, 'allowed_domains', None)
        if domain:
            data = db.query('''select url from t_hh_proxy_list where domain ="{}" 
                and valid>0 order by update_time desc'''.format(domain[0]))
            if data:
                proxy_res = []
                for item in data:
                    proxy_res.append(item['url'])
                return proxy_res
        return []
