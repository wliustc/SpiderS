# coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import sys
import json
import web
data_cateType_dic = {
    '0': "全网排名",
    '1': "一级领域排名",
    '2': "二级领域排名"
}
result = ['firCateName', 'cateType', 'isDisplay', 'cateId', 'appId',
          'rank', 'arithId', 'status', 'createdDate',
          'statDate', 'secCateName', 'id', 'cateTypeName']

rr_ll = []
db = web.database(dbn='mysql', db='hillinsight', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
def parse(line):
    line_json = json.loads(line)
    content = line_json.get('content')
    content = json.loads(content)
    datas = content.get('datas')
    if datas:
        appRankList = datas.get('appRankList')
        if appRankList:
            appRankList = appRankList[0]
            cateRanks = appRankList.get('cateRanks')
            if cateRanks:
                appRanks = cateRanks[0]
                if appRanks:
                    appRanks = appRanks.get('cateRank')
                    if appRanks:
                        for apprank in appRanks:
                            # print apprank['cateType']
                            apprank['cateTypeName'] = data_cateType_dic.get(str(apprank['cateType']))
                            for ar in apprank:
                                if ar not in result:
                                    # print ar
                                    apprank.pop(ar)

                            for rs in result:

                                if not apprank.get(rs):
                                    # print apprank.get(rs)
                                    apprank[rs] = ''
                                    # print apprank.get(rs)
                            # print json.dumps(apprank)
                            db.insert('t_spider_qianfan_scale_rank',**apprank)
                            # rr_ll.append(apprank)
                            lll = []
                            # for ap,val in apprank.items():
                            #     lll.append(val)
                            #
                            # print lll
                            # if len(apprank)!=13:
                            #     print len(apprank)


for line in sys.stdin:
    parse(line)
# db.multiple_insert('t_spider_qianfan_scale_rank' ,rr_ll)
