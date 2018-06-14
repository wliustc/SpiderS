#-*- encoding:utf-8 -*-
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
#插入到mysql用这个。
for line in sys.stdin:
    print line