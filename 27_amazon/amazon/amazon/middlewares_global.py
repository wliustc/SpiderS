import random
import base64
from hillinsight.storage import dbs
db = dbs.create_engine('hillinsight', master=True, online=False)

    
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
    def __init__(self,domain):
        self.proxys = ''
    def process_request(self, request, spider):
        if not self.proxys:
            self.proxys = self._get_proxy(spider)
        if self.proxys:
            proxy = random.choice(self.proxys)
            if  random.random() < 0.0001:
                self.proxys = self._get_proxy(spider)
            request.meta['proxy'] = "%s" % proxy
    def _get_proxy(self,spider):
        domain = getattr(spider, 'allowed_domains', None)
        if domain:
            data = db.query('''select url from t_hh_proxy_list where domain ="{}" 
                and valid>0 order by update_time desc;'''.format(domain))
            if data:
                return [ item['url'] for item in data ]
        return []