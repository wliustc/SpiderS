import sys
import json
import web
import time
# db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
dt = time.strftime('%Y-%m-%d', time.localtime())
for line in sys.stdin:
    try:
        json_line = json.loads(line)
        response_content  = json_line.get('response_content')
        # print response_content
        response_content  = json.loads(response_content)
        # print response_content
        data = response_content.get('data')
        if data:
            list = data.get('list')
            if list:
                for ll in list:
                    group = ll.get('group')
                    groupId = ll.get('groupId')
                    modules = ll.get('modules')
                    if modules:
                        for module in modules:
                            result_div = {}
                            result_div['group_pe'] = group
                            result_div['groupId'] = groupId


                            module_id = module.get('id')
                            module_name = module.get('name')
                            followCount = module.get('followCount')
                            topicCount = module.get('topicCount')
                            desc = module.get('desc')
                            leaderTitle =module.get('leaderTitle')
                            bulletin = module.get('bulletin')
                            cntDay = module.get('cntDay')

                            result_div['module_id'] = module_id
                            result_div['module_name'] = module_name
                            result_div['followCount'] = followCount
                            result_div['topicCount'] = topicCount
                            result_div['desc_pe'] = desc
                            result_div['leaderTitle'] = leaderTitle
                            result_div['bulletin'] = bulletin
                            result_div['cntDay'] = cntDay
                            result_div['task_time'] = dt
                            print json.dumps(result_div)



        # res = db.insert('t_hh_dianping_shop_comments_test_tmp', **json_line)
        # print line
    except Exception,e:
        # print e
        pass
    