import sys
import json
import web
import time
# db = web.database(dbn='mysql', db='o2o', user='writer', pw='hh$writer', port=3306, host='10.15.1.24')
dt = time.strftime('%Y-%m-%d', time.localtime())
for line in sys.stdin:
    try:
        json_line = json.loads(line)
        # print json_line
        response_content  = json_line.get('response_content')
        # print response_content
        response_content  = json.loads(response_content)
        # print response_content
        List = response_content.get('List')
        # print List
        if List:
            for ll in List:
                # print ll
                item = {}
                item['category'] = json_line.get('category')
                item['category_child'] = json_line.get('category_child')
                item['task_time'] = dt
                for key,val in ll.items():

                    item[key]=val
                print json.dumps(item)
        # else:
        #     print response_content


        # res = db.insert('t_hh_dianping_shop_comments_test_tmp', **json_line)
        # print line
    except Exception,e:
        print e
        # pass